from metaservlet.api import delete_project, project_exists


def main(projects: list):
  for project in projects:
    print('-----', project)
    try:
      if not project_exists(project[0]):
        raise Exception(f'A project called {project[0]} does not exist')
      delete_project(project[0])
    except Exception as e:
      print('ERROR: ', e.args)
      continue