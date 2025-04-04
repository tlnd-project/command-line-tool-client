from metaservlet.api import user_group_exist, project_exists, create_authorization, delete_authorization

def main(authorizations: list):
  for authorization in authorizations:
    print('-----', authorization)
    type, project_name, group_name = authorization
    try:
      if not project_exists(project_name):
        raise Exception(f'A project called {project_name} does not exist')
      if not user_group_exist(group_name):
        raise Exception(f'A user group called "{group_name}" does not exist')
      delete_authorization(project_name, group_name)
      create_authorization(project_name, group_name, type)
    except Exception as e:
      print('ERROR: ', e.args)
      continue
