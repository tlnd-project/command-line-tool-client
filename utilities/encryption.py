import subprocess
import os.path


JAR_APP = 'dtcc.jar'


def decrypt(word: str, key_name: str) -> str:
  if not os.path.isfile(f'./{JAR_APP}'):
    raise Exception('Jar application to decrypt current value is not available')
  
  command = f'java -jar {JAR_APP} decrypt {key_name} "{word}"'
  try:
    return subprocess.check_output(
      command,
      shell = True,
      executable = '/bin/sh',
      stderr = subprocess.STDOUT
    ).decode('utf8').strip()
  except subprocess.CalledProcessError as cpe:
    raise Exception(cpe.output)
