import os
import sys
from dotenv import load_dotenv, find_dotenv

from utilities.encryption import decrypt
from utilities.bitbucket_files_management import BitbucketFileManager
from settings.constant import (
  CURRENT_HOST_NAME,
  PATH_FILE_ENV,
  PATH_FILE_KEYS_ENV,
  PATH_CACHE_DIRECTORY,
  PATH_FILE_KEY_BITBUCKET,
  PATH_FILE_DTCC_JAR,
  ENVIRONMENT_FLAG
)


def init_setup():

  def load_env_file(file_path):
    env_vars = {}
    with open(file_path, "r", encoding="utf-8") as f:
      for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
          continue
        if "=" in line:
          key, val = line.split("=", 1)
          env_vars[key.strip()] = val.replace('"', "").strip()
    return env_vars

  load_dotenv(dotenv_path=PATH_FILE_KEYS_ENV)
  token = decrypt(
    os.environ.get('REPOSITORY_KEYS_TOKEN'),
    PATH_FILE_KEY_BITBUCKET,
    PATH_FILE_DTCC_JAR,
  )
  client_bitbucket = BitbucketFileManager(
    url=os.environ.get('REPOSITORY_KEYS_URL'),
    branch=os.environ.get('REPOSITORY_KEYS_BRANCH'),
    auth_token=token
  )

  # 1) download .env file from bitbucket

  try:
    client_bitbucket.download_file(
      name_file="__all__",
      full_name_file=f"{ENVIRONMENT_FLAG}/__all__",
      output_path_file=PATH_CACHE_DIRECTORY
    )
    client_bitbucket.download_file(
      name_file=f".{CURRENT_HOST_NAME}",
      full_name_file=f"{ENVIRONMENT_FLAG}/.{CURRENT_HOST_NAME}",
      output_path_file=PATH_CACHE_DIRECTORY
    )
    path_file_env_all = f"{PATH_CACHE_DIRECTORY}/__all__"
    path_file_env_current_host_name = f"{PATH_CACHE_DIRECTORY}/.{CURRENT_HOST_NAME}"

    # TODO: add validation if the file exist
    env_vars = load_env_file(path_file_env_all)
    env_vars.update(load_env_file(path_file_env_current_host_name))

    for key, value in env_vars.items():
      tmp_token = env_vars[key].strip()
      if tmp_token[:1] == "#":
        name_key = tmp_token[1:]
        client_bitbucket.download_file(
          name_file=f"{name_key}.token",
          full_name_file=f"{ENVIRONMENT_FLAG}/keys/{name_key}",
          output_path_file=PATH_CACHE_DIRECTORY
        )
        path_file_token = f"{PATH_CACHE_DIRECTORY}/{name_key}.token"
        path_file_key = f"{PATH_CACHE_DIRECTORY}/{name_key}.key"
        token_encrypt = open(path_file_token).read().strip()

        open(path_file_key, "w").write(name_key)
        _token = decrypt(
          token_encrypt,
          path_file_key,
          PATH_FILE_DTCC_JAR,
        )
        env_vars[key] = _token
        os.remove(path_file_token)
        os.remove(path_file_key)
    # remove __all__ and .hostname
    os.remove(path_file_env_all)
    os.remove(path_file_env_current_host_name)

    # create the .env file
    with open(f"{PATH_CACHE_DIRECTORY}/.env", "w", encoding="utf-8") as f:
      for key, val in env_vars.items():
        f.write(f"export {key}={val}\n")

  except Exception as e:
    # 2) check if exists the file .env inside the `path_cache_directory`
    if not os.path.exists(PATH_FILE_ENV):
      raise Exception(
        """Environment files does not exist and  
        could not be downloaded from Bitbucket."""
      )

def main():
  from automation.automation_core import run_command
  from settings.credentials import (
    BITBUCKET_DATA_SOURCE_URL,
    BITBUCKET_DATA_SOURCE_BRANCH,
    BITBUCKET_DATA_SOURCE_TOKEN
  )

  command = sys.argv[1]
  batch_csv_source = sys.argv[2]

  client_bitbucket = BitbucketFileManager(
    url=BITBUCKET_DATA_SOURCE_URL,
    branch=BITBUCKET_DATA_SOURCE_BRANCH,
    auth_token=BITBUCKET_DATA_SOURCE_TOKEN
  )

  #1. Load module (required command).
  module_path = f'automation.command.{command}'
  module_service = __import__(module_path, fromlist=['object'])
  command_function = getattr(module_service, 'process_item')

  #2. Load remote CSV.
  data_list = client_bitbucket.list_csv_file_rows(
    f"{ENVIRONMENT_FLAG}/{batch_csv_source}"
  )
  # TODO: add verification WARNING. if the "sso" in TAC_URL, maybe crashed the run command

  #3. Run process.
  run_command(command_function, data_list)

if __name__ == "__main__":
  init_setup()
  main()
