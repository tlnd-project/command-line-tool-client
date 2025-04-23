import subprocess
import os.path


def decrypt(word: str, key_path: str, jar_path: str) -> str:
  if not os.path.isfile(jar_path):
    raise Exception('Jar application to decrypt current value is not available')
  
  command = f'java -jar {jar_path} decrypt {key_path} "{word}"'
  try:
    output = subprocess.check_output(
      command,
      shell = True,
      executable = '/bin/sh',
      stderr = subprocess.STDOUT
    ).decode('utf8').strip()
    if 'error' in output.lower() or 'exception' in output.lower():
      raise Exception(output)
  except subprocess.CalledProcessError as cpe:
    raise Exception(cpe.output)
