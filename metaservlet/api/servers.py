from metaservlet.core import call_metaservlet
from settings.logger_config import logging


logger = logging.getLogger(__name__)


def list_server() -> dict:
  """
  Get a list of servers using the MetaServlet API.

  Example of the retrieve data and return.
    {
      "result": [
        {
          "active": bool,
          "description": str,
          "fileTransferPort": int,
          "host": str,
          "id": int,
          "label": str,
          "monitoringPort": int,
          "port": int,
          "processMessagePort": int,
          "timeOutUnknowState": int,
          "timeZone": str,
          "useSSL": bool,
        }
      ]
      ... other keys
    }
  """
  return call_metaservlet('listServer')


def list_virtual_servers() -> dict:
  """
  Get a list of virtual servers using the MetaServlet API.

  Example of the retrieve data and return.
  {
    "result": [
      {
        "description": "",
        "id": int,
        "label": str,
        "servers": [
          {
            "serverId": int,
            "serverLabel": str,
          }
        ],
        "timezone": str,
      }
    ]
    ... other keys
  }
  """
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


def remove_server(server_id: int) -> dict:
  request_params = {
    'serverId': server_id,
  }
  return call_metaservlet('removeServer', request_params)


def remove_virtual_server(server_virtual_id: int) -> dict:
  request_params = {
    'id': server_virtual_id,
  }
  return call_metaservlet('removeVirtualServer', request_params)


def remove_servers_from_virtual_server(servers: list, server_virtual_id: str) -> dict:
  """
  Remove servers from a virtual server

  for example the value of the servers is:
    "servers": [
      {'serverId': '1'},
      {'serverId': '2'},
    ]
  """
  request_params = {
    'servers': servers,
    'virtualServerId': server_virtual_id,
  }
  return call_metaservlet('removeServersFromVirtualServer', request_params)
