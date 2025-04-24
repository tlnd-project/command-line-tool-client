from metaservlet.core import call_metaservlet


def list_server() -> dict:
  return call_metaservlet('listServer')


def list_virtual_servers() -> dict:
  return call_metaservlet('listVirtualServers')


def add_server(server_name: str, server_description: str, server_host: str) -> dict:
  request_params = {
    'label': server_name,
    'description': server_description,
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


def add_virtual_server(virtual_server_name: str,  virtual_server_description: str,) -> dict:
  request_params = {
    'label': virtual_server_name,
    'description': virtual_server_description,
    'timezone': 'America/New_York',
  }
  return call_metaservlet('createVirtualServer', request_params)


def add_server_to_virtual_server(server_id: int, virtual_server_id: int) -> dict:
  request_params = {
    'virtualServerId': virtual_server_id,
    'servers': [{'serverId': server_id}],
  }
  return call_metaservlet('addServersToVirtualServer' , request_params)


def create_project_server_authorization(project_name: str, cluster_name: str) -> dict:
  request_params = {
    'isVirtualServer': True,
    'projectName': project_name,
    'serverName': cluster_name,
  }
  return call_metaservlet('createServerProjectAuthorization' , request_params)


def remove_project_server_authorization(project_name: str, cluster_name: str) -> dict:
  request_params = {
    'isVirtualServer': True,
    'projectName': project_name,
    'serverName': cluster_name,
  }
  return call_metaservlet('removeServerProjectAuthorization' , request_params)
