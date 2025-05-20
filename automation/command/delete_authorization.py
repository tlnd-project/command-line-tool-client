from metaservlet.api import delete_authorization, project_exists, user_group_exist


def process_item(authorization: list):
  project_name, group_name = authorization

  if not project_exists(project_name):
    raise Exception(f'A project called {project_name} does not exist')
  if not user_group_exist(group_name):
    raise Exception(f'A user group called "{group_name}" does not exist')
  delete_authorization(project_name, group_name)
