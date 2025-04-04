from metaservlet.api import project_exists, create_project


def main(projects: list):
  for project in projects:
    print('-----', project)
    continue
    project_name, storage, git_location, git_login, git_pass = project
    try:
      if not project_exists(project_name):
        create_project(
          project_name, storage, git_location, git_login, git_pass
        )
      else:
        raise Exception(f'{project_name} already exist')
    except Exception as e:
      print('ERROR: ', e.args)
      continue