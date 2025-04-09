import subprocess
from utilities.files_management import download_file, build_file_url
import os.path


KEY_NAME = 'dtcc.key'
JAR_APP = 'dtcc.jar'


def load_key():
  if os.path.isfile(f'./{KEY_NAME}'):
    return
  key_url = build_file_url(KEY_NAME)
  key_content = download_file(key_url)
  with open(f'./{KEY_NAME}', 'w') as key_file:
    key_file.write(key_content)


def decrypt(word: str) -> str:
  load_key()
  if not os.path.isfile(f'./{JAR_APP}'):
    raise Exception('Jar application to decrypt current value is not available')
  
  command = f'java -jar {JAR_APP} decrypt {KEY_NAME} "{word}"'
  try:
    return subprocess.check_output(
      command,
      shell = True,
      executable = '/bin/sh',
      stderr = subprocess.STDOUT
    ).decode('utf8').strip()
  except subprocess.CalledProcessError as cpe:
    raise Exception(cpe.output)
