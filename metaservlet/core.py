import re
import ast
import json
import requests
import shortuuid
import subprocess
from urllib.parse import urlparse

from typing import Any, Dict, Optional, List, Tuple
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import settings.credentials as env
from metaservlet.scrapper.get_function_token import get_function_tokens
from metaservlet.error_codes import METASERVLET_ERROR_DICTIONARY
from settings.logger_config import logging


logger = logging.getLogger(__name__)

function_tokens = get_function_tokens()


class MetaservletException(Exception):
    pass


def call_metaservlet(action_name: str, params: Optional[Dict[str, Any]] = None) -> dict:
  request_to_log = {**params} if params else {}
  request_id = shortuuid.uuid()
  logger.info(f'Command({request_id}): {action_name}')

  request = {
    'actionName': action_name,
    'authPass': env.TALEND_PASSWORD,
    'authUser': env.TALEND_USER, 
    **params
  }

  request_json_str = json.dumps(request).replace('"',"'")
  command=(
    f'{env.METASERVLET_CALLER}'
    f' --tac-url={env.TALEND_URL}'
    f' --json-params="{request_json_str}"'
  )

  try:
    result = subprocess.check_output(
      command,
      shell = True,
      executable = '/bin/sh',
      stderr = subprocess.STDOUT
    )
    print(f'Response({request_id}): ', result.splitlines()[0])
    print('')
    json_result = json.loads(result.splitlines()[0])
    if 'error' in json_result:
      raise MetaservletException(
        json_result['error'],
        json_result["returnCode"],
        json_result,
      )
    if json_result["returnCode"] in METASERVLET_ERROR_DICTIONARY:
      raise MetaservletException(
        METASERVLET_ERROR_DICTIONARY[json_result["returnCode"]],
        json_result["returnCode"],
        json_result,
      )
    return json_result
  except subprocess.CalledProcessError as cpe:
    raise Exception(cpe.output, -1, {})


class TACHttpClient:
  """This class implement request for Talend Administration Center TAC.
  this service is based with GWT-RPC Protocol version 7."""

  def __init__(self, base_url=None, retries=3, backoff_factor=0.3, timeout=5.0):
    """backoff_factor:  How time to need to await in each retry, before to retry against the request """
    # remove the slash in the end of the url.
    self.base_url = base_url.rstrip("/") if base_url else ""
    self.GWT_PROTOCOL_VERSION = "7"
    self.GWT_BASE_URL = self.base_url + "/administrator/"
    self.GWT_TAC_PERMUTATION = "17B18BA3641F02EA98896D1400E44444"
    self.xsrf_token = None
    self.timeout = timeout
    self.session = requests.Session()
    _parsed = urlparse(self.base_url)
    self.hostname = _parsed.hostname
    self.host = _parsed.netloc
    self.origin = f"{_parsed.scheme}://{self.host}"
    self.session.headers.update({
      "User-Agent": "PythonHTTPClient/1.0",
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br, zstd',
      'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
      'Host': self.host,
      'Origin': self.origin,
      'Referer': f"{self.base_url}/"
    })

    retry_strategy = Retry(
      total=retries,
      backoff_factor=backoff_factor,
      status_forcelist=[429, 500, 502, 503, 504],
      allowed_methods=["GET", "POST", "PUT", "DELETE"],
      raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    self.session.mount("http://", adapter)
    self.session.mount("https://", adapter)

  def _build_url(self, endpoint):
    return f"{self.base_url}/{endpoint.lstrip('/')}"

  @staticmethod
  def _handle_response(response):
    if 200 <= response.status_code < 300:
      # TODO: parse response.text //OK
      print("[Response]: ", response.status_code)
      try:
        print(response.text)
      except AttributeError as e:
        print("Not found <response.text>")
      return response
    else:
      print(f"HTTP {response.status_code}: {response.text}")
      return None

  def _build_gwt_rpc_body(
      self,
      *,
      serialization_policy_id: str,
      total_params: str,
      token_manifest: str,
      service_interface: str,
      method_name: str,
      extra_params: List[str],
      xsrf: Optional[Tuple[str, str]]=None,
      version_protocol: Optional[str]=None,
      gwt_base_url: Optional[str]=None,
  ):
    xsrf_token = f"|{xsrf[0]}|{xsrf[1]}" if xsrf else f""
    return (
      f"{version_protocol or self.GWT_PROTOCOL_VERSION}"
      f"|{serialization_policy_id}"
      f"|{total_params}"
      f"|{gwt_base_url or self.GWT_BASE_URL}"
      f"|{token_manifest}"
      f"{xsrf_token}"
      f"|{service_interface}"
      f"|{method_name}"
      "|" + "|".join(extra_params) + "|"
    ).encode("utf-8")

  def get(self, endpoint, params=None, headers=None):
    url = self._build_url(endpoint)
    try:
      response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
      return self._handle_response(response)
    except requests.RequestException as e:
      print(f"[GET] Error: {e}")
      return None

  def post(self, endpoint=None, full_url=None, data=None, headers=None, **kwargs):
    """
    :param endpoint: only the resource
    :type endpoint: str
    :param full_url: all url. is mutually exclusive with endpoint
    :type full_url: str
    """
    print("<=== Request POST ===>")
    print("[Body]", data)
    print("[Headers Param]", headers)
    print("[Headers session]", self.session.headers)
    print("[URL]", full_url or self._build_url(endpoint))
    print("[Cookies] ", self.session.cookies)
    for cookie in self.session.cookies:
      print("\t name: ", cookie.name, " value: ", cookie.value, " domain: ", cookie.domain, " path: ", cookie.path )
    try:
      response = self.session.post(
        full_url or self._build_url(endpoint),
        data=data,
        headers=headers,
        timeout=self.timeout,
        **kwargs
      )
      return self._handle_response(response)
    except requests.RequestException as e:
      print(f"[POST] Error: {e}")
      return None

  def login(self, username, password):
    print("Getting login ...")
    manifest_token = function_tokens[
      'org.talend.gwttoolkit.client.login.service.LoginService'
    ]
    request_binary_body = self._build_gwt_rpc_body(
      serialization_policy_id="0",
      total_params="7",
      token_manifest=manifest_token,
      service_interface="org.talend.gwttoolkit.client.login.service.LoginService",
      method_name="login",
      extra_params=[
        'java.lang.String/2004016611',
        username,
        password,
        '1', '2', '3', '4', '2', '5', '5', '6', '7'
      ]
    )
    response = self.post(
      endpoint="administrator/login",
      data=request_binary_body,
      verify=False,
      allow_redirects=True
    )
    # TODO: valid Exception
    # //EX[0,5,4,3,2,2,0,1, ["org.domain.gwttoolkit.client.exception.ClientBusinessException/000000000", "[Ljava.lang.String;/3242423234", "user@domain.com", "web", "userCache.alreadyLogged" ], 0,7]
    # TODO: valid OK, then set the session, verify if set Cookie in headers
    # //OK[53,...,0,7]
    print("Ending login ...\n\n")

  def get_xsrf_token(self):
    print("Getting XSRF token ...")
    manifest_token = function_tokens[
      'com.google.gwt.user.client.rpc.XsrfTokenService'
    ]
    request_binary_body = self._build_gwt_rpc_body(
      serialization_policy_id="0",
      total_params="4",
      token_manifest=manifest_token,
      service_interface="com.google.gwt.user.client.rpc.XsrfTokenService",
      method_name="getNewXsrfToken",
      extra_params=[
        '1', '2', '3', '4', '0'
      ]
    )
    headers = {
      'X-GWT-Module-Base': self.GWT_BASE_URL,
      'X-GWT-Permutation': self.GWT_TAC_PERMUTATION,
    }
    response = self.post(
      endpoint="administrator/xsrf",
      data=request_binary_body,
      headers=headers,
      verify=False,
      allow_redirects=True
    )
    # TODO: raise custom Exception when the response.text has not //OK string
    # //OK[2,1,["com.google.gwt.user.client.rpc.XsrfToken/0000000000", "<token: 32 digit HEX>"],0,7]
    _aux = ast.literal_eval(response.text.replace("//OK", ""))
    self.xsrf_token = (_aux[2][0], _aux[2][1])  # [2][0] = "com.google.gwt.user.client.rpc.XsrfToken/0000000000" [2][1] = "token:32"
    print("Ending XSRF token ...\n\n")

  def configuration_update_field(self, id_field: str, value: str):
    print("Updating configuration field ...")
    manifest_token = function_tokens[
      'org.talend.gwtadministrator.client.module.settings.configuration.service.ConfigService'
    ]
    request_binary_body = self._build_gwt_rpc_body(
      serialization_policy_id="2",
      total_params="9",
      token_manifest=manifest_token,
      xsrf=self.xsrf_token,
      service_interface="org.talend.gwtadministrator.client.module.settings.configuration.service.ConfigService",
      method_name="saveConfigValue",
      extra_params=[
        'org.talend.gwtadministrator.client.module.settings.configuration.model.enums.Config/3074497691',
        'java.lang.String/2004016611',
        value,
        '1', '2', '3', '4', '5', '6', '2', '7', '8', '7', id_field, '9'
      ]
    )
    headers = {
      'X-GWT-Module-Base': self.GWT_BASE_URL,
      'X-GWT-Permutation': self.GWT_TAC_PERMUTATION,
    }
    response = self.post(
      endpoint="administrator/config",
      data=request_binary_body,
      headers=headers,
      verify=False,
      allow_redirects=True
    )
    print("Ending configuration field ...\n\n")

  def logout(self):
    print("Start Logout ...")
    manifest_token = function_tokens[
      'org.talend.gwttoolkit.client.login.service.LoginService'
    ]
    request_binary_body = self._build_gwt_rpc_body(
      serialization_policy_id="0",
      total_params="4",
      token_manifest=manifest_token,
      service_interface="org.talend.gwttoolkit.client.login.service.LoginService",
      method_name="logout",
      extra_params=[
        '1', '2', '3', '4', '0'
      ]
    )
    response = self.post(
      endpoint="administrator/login",
      data=request_binary_body,
      verify=False,
      allow_redirects=True
    )
    print("Ending Logout ...\n\n")



class TACHttpClientSSO:
  def __init__(self, sso_url=None):
    self.sso_url=sso_url

  def login(self, username, password):
    print("Getting login SSO...")
    sso_session = requests.Session()
    response = sso_session.post(
      url=self.sso_url,
      verify=False
    )
    # TODO: add validator if the return url is not the same with the TALEND_URL
    # TODO: add try except if no exist group or if response has not text
    sso_url_partial = re.search(
      '/idp/.*/resumeSAML20/idp/startSSO\.ping',
      response.text
    ).group()
    headers_sso_login = {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
    request_body = (
      f'pf.username={username}'
      f'&pf.pass={password}'
      f'&pf.ok=clicked'
      f'&pf.cancel='
      f'&pf.adapterId=corpADAdpater'
    )
    url_parse = urlparse(self.sso_url)
    sso_login_response = sso_session.post(
      url=f'{url_parse.scheme}://{url_parse.netloc}{sso_url_partial}',
      data=request_body,
      headers=headers_sso_login,
      verify=False,
    )

    match2 = re.search('action="(.*)"\>', sso_login_response.text)
    sso_redirect_url = match2.group(1)
    match3 = re.search('name="SAMLResponse" value="(.*)"', sso_login_response.text)
    sso_login_key = match3.group(1)

    login_redirect = sso_session.post(
      url=sso_redirect_url,
      data={'SAMLResponse': sso_login_key},
      headers=headers_sso_login,
      verify=False,
      allow_redirects=False
    )
    # TODO: login_redirect a redirect is expected 302 login_redirect

    tac_client = TACHttpClient(base_url=sso_redirect_url.replace("ssologin", ""))
    tac_client.session.cookies.set('JSESSIONID', sso_session.cookies.get('JSESSIONID'), domain=tac_client.hostname)
    # tac_client.session.headers.update({"JSESSIONID": sso_session.cookies.get('JSESSIONID')})
    return tac_client
