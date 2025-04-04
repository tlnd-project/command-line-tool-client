from metaservlet.api import project_exists, create_project


def main(projects: list):
  for project in projects:
    print('-----', project)
    project_name, storage, git_location, git_login, git_pass = project
    try:
      create_project(
        project_name, storage, git_location, git_login, git_pass
      )
    except Exception as e:
      print('ERROR: ', e.args)
      continue