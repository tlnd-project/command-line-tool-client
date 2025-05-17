import json
import requests
import shortuuid
import subprocess

from typing import Any, Dict, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import settings.credentials as env
from metaservlet.error_codes import METASERVLET_ERROR_DICTIONARY


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


class HTTPClient:
  def __init__(self, base_url=None, retries=3, backoff_factor=0.3, timeout=5.0):
    """backoff_factor:  How time to need to await in each retry, before to retry against the request """
    self.base_url = base_url.rstrip("/") if base_url else ""  # remove the slash in the end of the url.
    self.timeout = timeout

    self.session = requests.Session()
    # self.session.cookies.set('talendremember', 'false')
    # self.session.cookies.set('lang', 'en')
    self.session.headers.update({
      "User-Agent": "PythonHTTPClient/1.0",
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br, zstd',
      'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
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

  def _handle_response(self, response):
    if 200 <= response.status_code < 300:
      try:
        return response.json()
      except ValueError:
        return response.text
    else:
      print(f"HTTP {response.status_code}: {response.text}")
      return None

  def get(self, endpoint, params=None, headers=None):
    url = self._build_url(endpoint)
    try:
      response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
      return self._handle_response(response)
    except requests.RequestException as e:
      print(f"[GET] Error: {e}")
      return None

  def post(self, endpoint, data=None, headers=None, json_data=False, **kwargs):
    url = self._build_url(endpoint)
    try:
      if json_data:
        response = self.session.post(url, json=data, headers=headers, timeout=self.timeout, **kwargs)
      else:
        response = self.session.post(url, data=data, headers=headers, timeout=self.timeout, **kwargs)
      return self._handle_response(response)
    except requests.RequestException as e:
      print(f"[POST] Error: {e}")
      return None


tac_client = HTTPClient(base_url=env.TALEND_URL)
