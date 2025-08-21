from metaservlet.api import project_exists, create_project
from utilities.encryption import decrypt
from settings.constant import path_file_dtcc_jar, path_file_key


def process_item(project: list):
  project_name, storage, git_location, git_login, git_pass = project

  if project_exists(project_name):
    raise Exception(f'{project_name} already exist')
  
  if storage=='git':
    git_pass = decrypt(git_pass, path_file_key, path_file_dtcc_jar)
  
  create_project(
    project_name, storage, git_location, git_login, git_pass
  )
 