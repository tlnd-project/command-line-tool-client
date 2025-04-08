import requests
import subprocess
from settings.credentials import (
  BITBUCKET_AUTH_TOKEN, BITBUCKET_REPO_URL, ENVIRONMENT_FLAG
)

KEY_FILE_NAME = 'tmp-key.key'


def load_key():
  headers = {
    'Authorization': f'Bearer {BITBUCKET_AUTH_TOKEN}'
  }
  key_url = BITBUCKET_REPO_URL.format(f'{ENVIRONMENT_FLAG}/dtcc.key')
  response = requests.get(
    key_url, verify=False, allow_redirects=True, headers=headers
  )
  with open('tmp-key.key') as key_file:
    key_file.write(response.text)


def decrypt(word: str) -> str:
  command = f'java -jar dtcc.jar decrypt {KEY_FILE_NAME} "{word}"'
  try:
    return subprocess.check_output(
      command,
      shell = True,
      executable = '/bin/sh',
      stderr = subprocess.STDOUT
    )
  except subprocess.CalledProcessError as cpe:
    raise Exception(cpe.output)