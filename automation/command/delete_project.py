from metaservlet.api import delete_project, project_exists


def process_item(project: list):
  if not project_exists(project[0]):
    raise Exception(f'A project called {project[0]} does not exist')
  delete_project(project[0])
