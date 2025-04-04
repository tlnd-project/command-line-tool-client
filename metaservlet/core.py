import json
import settings.credentials as env
import subprocess
import shortuuid


def call_metaservlet(action_name: str, params: dict = {}) -> dict:
  request_to_log = {**params}
  request_id = shortuuid.uuid()
  print(f'Command({request_id}): {action_name}')
  print(f'Request({request_id}): ', request_to_log)

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
    json_result = json.loads(result.splitlines()[0])
    if 'error' in json_result:
      raise Exception(json_result['error'])
    return json_result
  except subprocess.CalledProcessError as cpe:
    raise Exception(cpe.output)
