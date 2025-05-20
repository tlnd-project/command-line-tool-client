from metaservlet.api import create_project, project_exists
from settings.credentials import JAR_DECRYPTION_PATH
from utilities.bitbucket_files_management import download_file
from utilities.encryption import decrypt

KEY_NAME = 'dtcc.key'


def process_item(project: list):
  project_name, storage, git_location, git_login, git_pass = project

  if project_exists(project_name):
    raise Exception(f'{project_name} already exist')

  if storage == 'git':
    key_path = download_file(KEY_NAME)
    git_pass = decrypt(git_pass, key_path, JAR_DECRYPTION_PATH)

  create_project(
      project_name, storage, git_location, git_login, git_pass
  )
