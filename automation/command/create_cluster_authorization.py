from metaservlet.api import project_exists, create_project_server_authorization


def process_item(authorization: list):
  project_name, server_name = authorization
  if not project_exists(project_name):
    raise Exception(f'A project called {project_name} does not exist')
  create_project_server_authorization(project_name, server_name)
