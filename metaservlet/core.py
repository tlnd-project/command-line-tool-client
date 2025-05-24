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


function_tokens = get_function_tokens()


class MetaservletException(Exception):
    pass


def call_metaservlet(action_name: str, params: Optional[Dict[str, Any]] = None) -> dict:
  request_to_log = {**params} if params else {}
  request_id = shortuuid.uuid()
  print(f'Command({request_id}): {action_name}')
  #print(f'Request({request_id}): ', request_to_log)

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
    self.GWT_BASE_URL = self.base_url + "/administrator"
    self.GWT_TAC_PERMUTATION = "17B18BA3641F02EA98896D1400E44444"
    self.xsrf_token = None
    self.timeout = timeout
    self.session = requests.Session()
    _parsed = urlparse(self.base_url)
    host = _parsed.netloc
    origin = f"{_parsed.scheme}://{host}"
    self.session.headers.update({
      "User-Agent": "PythonHTTPClient/1.0",
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br, zstd',
      'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
      'Host': host,
      'Origin': origin,
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
      return response.text
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
    return (
      f"{version_protocol or self.GWT_PROTOCOL_VERSION}"
      f"|{serialization_policy_id}"
      f"|{total_params}"
      f"|{gwt_base_url or self.GWT_BASE_URL}"
      f"|{token_manifest}"
      f"|{xsrf[0]}|{xsrf[1]}" if xsrf else ""
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
    endpoint -- only the resource
    full_url -- all url. is mutually exclusive with endpoint
    """
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
    print(response)

  def get_xsrf_token(self):
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
      'X-GWT-Module-Base': env.TALEND_URL + '/administrator/',
      'X-GWT-Permutation': self.GWT_TAC_PERMUTATION,
    }
    response = self.post(
      endpoint="administrator/xsrf",
      data=request_binary_body,
      headers=headers,
      verify=False,
      allow_redirects=True
    )
    print(response)
    _aux = ast.literal_eval(response.text.replace("//OK", ""))
    self.xsrf_token = (_aux[2][0], _aux[2][1])

  def configuration_update_field(self, id_field: str, value: str):
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
      'X-GWT-Module-Base': env.TALEND_URL + '/administrator/',
      'X-GWT-Permutation': self.GWT_TAC_PERMUTATION,
    }
    response = self.post(
      endpoint="administrator/config",
      data=request_binary_body,
      headers=headers,
      verify=False,
      allow_redirects=True
    )
    print(response)

  def logout(self):
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
    print(response)



class TACHttpClientSSO:
  def __init__(self, sso_url=None):
    self.sso_url=sso_url

  @staticmethod
  def login(self, username, password):
    sso_session = requests.Session()
    response = sso_session.post(
      url=self.sso_url,
      verify=False
    )
    pattern = '/idp/.*/resumeSAML20/idp/startSSO\.ping'
    # TODO: add validator if the return url is not the same with the TALEND_URL
    sso_url_partial = re.search(pattern, response.text).group()
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
    sso_login_response = sso_session.post(
      url=f'https://idpssod.dtcc.com{sso_url_partial}',
      data=request_body,
      headers=headers_sso_login,
      verify=False,
    )
    print(sso_login_response.text)
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
    print(login_redirect)
    tac_client = TACHttpClient(base_url=sso_redirect_url)
    tac_client.session.headers.update({"JSESSIONID": sso_session.cookies.get('JSESSIONID')})
    return tac_client
