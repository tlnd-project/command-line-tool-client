from collections.abc import Callable
from functools import reduce
from metaservlet.core import call_metaservlet
from metaservlet.api import (
  ms_add_server, ms_add_virtual_server, add_server_to_virtual_server
)


def exist_server_in_cluster(server_id: int, cluster: dict) -> bool:
  if not "servers" in cluster:
    return False

  for server in cluster['servers']:
    if server_id==server["serverId"]:
      return True

  return False


def add_server_to_cluster(server_id: int, cluster: dict):
  if not 'servers' in cluster:
    cluster['servers'] = [{'serverId': server_id}]
  else:
    cluster['servers'].append({'serverId': server_id})


def map_servers(servers: dict) -> list:
  return reduce(
    lambda acc,i: {f'i["label"]': i, **acc}, servers['result'], {}
  )


def create_server(server_name: str, servers_map: dict, add_server: Callable) -> int:
  if not server_name in servers_map:
    try:
      created_server = add_server()
      print('Server created from scratch')
      server_id = created_server['id']
      servers_map[server_name] = {'label': server_name, 'id': server_id}
    except:
      print('Needs manual intervention')
      raise Exception("")
  else:
    print("Server already exist")
    server_id = servers_map[server_name]['id']
  return server_id


def main(servers_lines: list):
  servers_map = map_servers(call_metaservlet('listServer'))
  clusters_map = map_servers(call_metaservlet('listVirtualServers'))

  for server in servers_lines:
    print('-----', server)
    server_name, server_host, cluster_name, match_flag = server

    #1. Create server.
    try:
      server_id = create_server(
        server_name, 
        servers_map,
        lambda: add_server(server_name, server_host)
      )
    except:
      continue

    #1. Create virtual server.
    try:
      cluster_id = create_server(
        cluster_name,
        clusters_map,
        lambda: ms_add_virtual_server(cluster_name)
      )
    except:
      continue

    #3. Add server to cluster.
    if match_flag=='1':
      cluster = clusters_map[cluster_name]
      if not exist_server_in_cluster(server_id, cluster):
        add_server_to_virtual_server(server_id, cluster_id) #remote add operation
        add_server_to_cluster(server_id, cluster) #local (in memory) add operation
        print (f'Server {server_id} added to cluster {cluster_id}')
      else:
        print (f'Server {server_id} already exist in cluster {cluster_id}')
