import os
import sys
from dotenv import load_dotenv, find_dotenv

from automation.automation_core import run_command
from utilities.encryption import decrypt
from utilities.bitbucket_files_management import BitbucketFileManager
from settings.constant import (
  CURRENT_HOST_NAME,
  ENV_NAME,
  ENV_KEYS_NAME,
  PATH_CACHE_DIRECTORY,
  PATH_FILE_KEY_BITBUCKET,
  PATH_FILE_DTCC_JAR,
  NAME_DTCC_KEY,
  NAME_DTCC_KEY_MASTER,
  NAME_DTCC_KEY_BITBUCKET,
  ENVIRONMENT_FLAG
)


def init_setup():

  load_dotenv(dotenv_path=ENV_KEYS_NAME)
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
      file_name=f"{ENVIRONMENT_FLAG}/{CURRENT_HOST_NAME}/{ENV_NAME}",
      path_file=PATH_CACHE_DIRECTORY
    )
    client_bitbucket.download_file(
      file_name=f"{ENVIRONMENT_FLAG}/{CURRENT_HOST_NAME}/{NAME_DTCC_KEY_MASTER}",
      path_file=PATH_CACHE_DIRECTORY
    )
    client_bitbucket.download_file(
      file_name=f"{ENVIRONMENT_FLAG}/{NAME_DTCC_KEY}",
      path_file=PATH_CACHE_DIRECTORY
    )
    client_bitbucket.download_file(
      file_name=f"{ENVIRONMENT_FLAG}/{NAME_DTCC_KEY_BITBUCKET}",
      path_file=PATH_CACHE_DIRECTORY
    )
  except Exception as e:
    # 2) check if exists the file .env inside the `path_cache_directory`
    if (
        not os.path.exists(os.path.join(PATH_CACHE_DIRECTORY, ENV_NAME))
        or not os.path.isdir(os.path.join(PATH_CACHE_DIRECTORY, NAME_DTCC_KEY))
        or not os.path.isdir(os.path.join(PATH_CACHE_DIRECTORY, NAME_DTCC_KEY_MASTER))
        or not os.path.isdir(os.path.join(PATH_CACHE_DIRECTORY, NAME_DTCC_KEY_BITBUCKET))
    ):
      raise Exception(
        """Environment files does not exist and  
        could not be downloaded from Bitbucket."""
      )

def main():
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
