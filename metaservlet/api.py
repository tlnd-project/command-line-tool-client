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
    'processMessagePort': 8555
  }
  return call_metaservlet('addServer', request_params)


def ms_add_virtual_server(virtual_server_name: str) -> dict:
  request_params = {
    'label': virtual_server_name,
    'description': '',
    'timezone': 'America/New_York'
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
    project_type = 'DI'
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
    'projectType': project_type
  }
  if storage=='git': 
    print(request_params)
  else:
    call_metaservlet('createProject' , request_params)


