from collections.abc import Callable
from functools import reduce
from metaservlet.core import call_metaservlet
import metaservlet.api as metaservlet


class LocalServerClusterManagment():
  servers_map: list = []
  clusters_map: list = []

  def __init__(self, servers, clusters):
    self.servers_map = self.make_data_map(servers)
    self.clusters_map = self.make_data_map(clusters)

  def make_data_map(self, servers: dict) -> list:
    return reduce(
      lambda acc,i: {i["label"]: i, **acc}, servers['result'], {}
    )

  def exist_server_in_cluster(self, server_id: int, cluster_name: str) -> bool:
    cluster = self.clusters_map[cluster_name]
    if not "servers" in cluster: return False
    for server in cluster['servers']:
      if server_id==server["serverId"]: return True
    return False

  def add_server_to_cluster(self, server_name: int, cluster_name: str):
    cluster = self.clusters_map[cluster_name]
    if not 'servers' in cluster: cluster['servers'] = []
    cluster['servers'].append(self.servers_map[server_name])

  def add_server_cluster(
    self, item_name: str, local_data_map: dict, remote_add_item_function: Callable
  ) -> int:
    if not item_name in local_data_map:
      remote_item_data = remote_add_item_function()
      item_id = remote_item_data['id']
      local_data_map[item_name] = {'label': item_name, 'id': item_id}

    return local_data_map[item_name]['id']

  def add_server(
    self, server_name: str, remote_add_server_function: Callable
  ) -> int:
    return self.add_server_cluster(
      server_name, self.servers_map, remote_add_server_function
    )

  def add_cluster(
    self, cluster_name: str, remote_add_server_function: Callable
  ) -> int:
    return self.add_server_cluster(
      cluster_name, self.clusters_map, remote_add_server_function
    )


local_storage = LocalServerClusterManagment(
  metaservlet.list_server(),
  metaservlet.list_virtual_servers()
)


def process_item(server: list):
  server_name, server_description, server_host, cluster_name, cluster_description, match_flag = server

  if server_name:
    server_id = local_storage.add_server(
      server_name,
      lambda: metaservlet.add_server(server_name, server_description, server_host)
    )
  if cluster_name:
    cluster_id = local_storage.add_cluster(
      cluster_name,
      lambda: metaservlet.add_virtual_server(cluster_name, cluster_description)
    )
  if (
    match_flag=='1' and 
    not local_storage.exist_server_in_cluster(server_name, cluster_name)
  ):
    metaservlet.add_server_to_virtual_server(server_id, cluster_id)
    local_storage.add_server_to_cluster(server_name, cluster_name)
