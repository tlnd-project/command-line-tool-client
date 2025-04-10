from metaservlet.core import call_metaservlet


def delete_authorization(
  project_name: str, 
  group_name: str, 
  authorization_entity: str='Group',
) -> dict:
  request_params = {
    'groupLabel': group_name,
    'projectName': project_name,
    'authorizationEntity': authorization_entity,
  }
  return call_metaservlet('deleteAuthorization', request_params)


def create_authorization(
  project_name: str,
  user_group_name: str,
  authorization_type: str,
  authorization_entity: str='Group',
) -> dict:
  if not project_name:
    raise Exception('Project name can not be empty.')
  if not user_group_name:
    raise Exception('User group name can not be empty.')
  if not authorization_type in ['ReadOnly', 'ReadWrite']:
    raise Exception('<storage> invalid value.')
  request_params = {
    'groupLabel': user_group_name,
    'projectName': project_name,
    'authorizationEntity': authorization_entity,
    'authorizationType': authorization_type,
  }
  return call_metaservlet('createAuthorization', request_params)