from metaservlet.api import project_exists, create_project


def process_item(project: list):
  project_name, storage, git_location, git_login, git_pass = project

  if project_exists(project_name):
    raise Exception(f'{project_name} already exist')
  create_project(
    project_name, storage, git_location, git_login, git_pass
  )
 