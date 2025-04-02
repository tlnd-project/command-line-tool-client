import subprocess, sys, ison, csv
from functools import reduce
from metaservlet.core import call_metaservlet


def ms_add_server(server_name: str, server_host: str) -> dict:
  params = {
    'label': server_name,
    'description': '',
    'host' server_host,
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


def exist_server_in_cluster(server_id: int, virtual_server: dict) -> bool:
  if not "servers" in virtual_server:
    return False

  for server in virtual_server['servers']:
    if server_id==server["serverId"]:
      return True

  return False


def add_server_to_virtual_server_map(server_id: int, virtual_server: dict):
  if not servers in virtual_server:
    virtual_server['servers']=[{'serverId': server_id}]
  else:
    virtual_server['servers'].append({'serverId': server_id})


def main():
  servers = call_metaservlet('listServer')
  servers_map = reduce(lambda acc,i: {f'i["label"]': i, **acc}, servers['result'], {})
  virtual_servers = call_metaservlet('listVirtualServer')
  virtual_servers_map = reduce(lambda acc,i: {f'i["label"]': i, **acc}, virtual_servers['result'], {})

  servers_lines = cv. reader (file, delimiter='|')
  for server in servers_lines:
    print('-----', Server)
    server_name, server_host, virtual_server_name, match_servers_flag = server
    if not server_name in servers_map:
      try:
        created server = ms_add_server(server_name, server_host)
        print('1. Create Server from scratch')
        server_id = created server['id']
        servers_map[server_name] = {'label': server_name, 'id': server_id}
      except:
        print('ERROR: «Step 1> Needs manual intervention')
        continue 
    else:
      print ("1. Server already exist")
      server_id = servers_map[server_name]['id']

    if not virtual_server_name in virtual_servers_map:
      try:
        created_virtual_server = ms_add_virtual_server(virtual_server_name)
        print("2. create virtual server from scratch")
        virtual_server_id = created_virtual_server['id']
        virtual_servers_map [virtual_server_name] = {
          'label': virtual_server_name,
          'id': virtual_server_id
        }
      except:
        print('ERROR: «Step 2s Needs manual intervention')
        continue
      else:
        virtual_server_id = virtual_servers_map[virtual_server_name]['id']
        print("2. Virtual server already exist ")

    if match_servers_flag=='1':
      if not exist_server_in_cluster(server_id, virtual_servers_map[virtual_server_name]):
        add_server_to_virtual_server(server_id, virtual_server_ id) add_server_to_virtual_server_map (server_id, virtual_servers_map [virtual_server_name]) 
        print (f'3. Server {server_id} added to cluster {virtual_server_id}')
      else:
        print (f'3. Server {server_id} already exist in cluster {virtual_server_id}')
