import json
import settings.credentials as env
import subprocess
import shortuuid
from metaservlet.error_codes import METASERVLET_ERROR_DICTIONARY


class MetaservletException(Exception):
    pass


def call_metaservlet(action_name: str, params: dict = {}) -> dict:
  request_to_log = {**params}
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
