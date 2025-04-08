from metaservlet.core import call_metaservlet


def ms_add_server(server_name: str, server_host: str) -> dict:
  request_params = {
    'label': server_name,
    'description': '',
    'host': server_host,
    'adminConsolePort': 8040,
    'commandPort': 8000,
    'filePort': 8001,
    'monitoringPort': 8888,
    'timeoutUnknownState': '120',
    'timezoneId': 'America/New_York',
    'processMessagePort': 8555,
  }
  return call_metaservlet('addServer', request_params)


def ms_add_virtual_server(virtual_server_name: str) -> dict:
  request_params = {
    'label': virtual_server_name,
    'description': '',
    'timezone': 'America/New_York',
  }
  return call_metaservlet('createVirtualServer', request_params)


def add_server_to_virtual_server(server_id: int, virtual_server_id: int) -> dict:
  request_params = {
    'virtualServerId': virtual_server_id,
    'servers': [{'serverId': server_id}],
  }
  return call_metaservlet('addServersToVirtualServer' , request_params)


def project_exists(project_name: str):
  if not project_name:
    raise Exception('Project name can not be empty.')
  request_params = {'projectName': project_name}
  response = call_metaservlet('projectExist' , request_params)
  return response['result']=='true'


def create_project(
    project_name: str,
    storage: str = 'none',
    git_location: str = '',
    git_login: str = '',
    git_password: str = '',
    project_type = 'DI',
):
  if not project_name:
    raise Exception('Project name can not be empty.')
  if not storage:
    raise Exception('<storage> can not be empty.')
  if not storage in ['git', 'none']:
    raise Exception('<storage> invalid value.')
  if storage == 'git':
    if not git_location:
      raise Exception('<git_location> can not be empty.')
    if not git_login:
      raise Exception('<git_login> can not be empty.')
    if not git_password:
      raise Exception('<git_password> can not be empty.')
  
  request_params = {
    'projectName': project_name,
    'storage': storage,
    'projectGitLocation': git_location,
    'gitLogin': git_login,
    'gitPassword': git_password,
    'projectType': project_type,
  }
  if storage=='git': 
    print(request_params)
  else:
    call_metaservlet('createProject' , request_params)


def delete_project(project_name: str) -> dict:
  if not project_name:
    raise Exception('Project name can not be empty.')
  request_params = {'projectName': project_name}
  return call_metaservlet('deleteProject', request_params)


def user_group_exist(user_group_name: str) -> int:
  if not user_group_name:
    raise Exception('User group name can not be empty.')
  request_params = {'label': user_group_name}
  response = call_metaservlet('getIdByUserGroupName', request_params)
  return response.get("id", 0)


def create_user_group(
  user_group_name: str, description: str, type:str='DQ'
) -> dict:
  if not user_group_name:
    raise Exception('User group name can not be empty.')
  request_params = {
    'label': user_group_name, 'type': type, 'description': description,
  }
  return call_metaservlet('createUserGroup', request_params)


def delete_user_group(user_group_id: int) -> dict:
  request_params = {'id': user_group_id}
  return call_metaservlet('deleteUserGroupById', request_params)


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


def user_exists(user_name: str):
  if not user_name:
    raise Exception('User name can not be empty.')
  request_params = {'userLogin': user_name}
  response = call_metaservlet('userExist' , request_params)
  return response['result']=='true'


def delete_user(user_name: str) -> dict:
  if not user_name:
    raise Exception('User name can not be empty.')
  request_params = {'userLogin': user_name}
  return call_metaservlet('deleteUser', request_params)


def set_license_key(license_key_path: str) -> dict:
  if not license_key_path:
    raise Exception('License key path can not be empty.')
  request_params = {'licenseKeyPath': license_key_path}
  return call_metaservlet('setLicenseKey', request_params)


def task_exist(task_name: str):
  if not task_name:
    raise Exception('Task name can not be empty')
  request_params = {'taskName': task_name}
  response = call_metaservlet('getTaskIdByName', request_params)
  return response.get("id", 0)


def update_task(task_id, context_name, value):
  if not context_name:
    raise Exception('Context name can not be empty')
  request_params = {'taskId': task_id, 'context': {f'{context_name}': value}}
  return call_metaservlet('updateTask', request_params)


def update_task_jvmparam(task_id, context_name, value):
  if not context_name:
    raise Exception('Context name can not be empty')
  request_params = {'taskId': task_id, 'context': {f'{context_name}': value}}
  return call_metaservlet('updateTaskParam', request_params)
