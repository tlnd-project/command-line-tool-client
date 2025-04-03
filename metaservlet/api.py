from metaservlet.core import call_metaservlet


def ms_add_server(server_name: str, server_host: str) -> dict:
  params = {
    'label': server_name,
    'description': '',
    'host': server_host,
    'adminConsolePort': 8040,
    'commandPort': 8000,
    'filePort': 8001,
    'timeoutUnknownState': '120',
    'timezoneId': 'America/New_York',
    'processMessagePort': 8555
  }
  return call_metaservlet('addserver', params)


def ms_add_virtual_server(virtual_server_name: str) -> dict:
  params = {
    'label': virtual_server_name,
    'description': '',
    'timezone': 'America/New_York'
  }
  return call_metaservlet('createvirtualserver', params)


def add_server_to_virtual_server(server_id: int, virtual_server_id: int) -> dict:
  params= {
    'virtualServerId': virtual_server_id,
    'servers': [{'serverId': server_id}],
  }
  return call_metaservlet('addServersToVirtualServer' , params)