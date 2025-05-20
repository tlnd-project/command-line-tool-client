from metaservlet.api import create_project_server_authorization, project_exists


def process_item(authorization: list):
  project_name, server_name = authorization
  if not project_exists(project_name):
    raise Exception(f'A project called {project_name} does not exist')
  create_project_server_authorization(project_name, server_name)
