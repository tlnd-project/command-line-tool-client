from collections.abc import Callable
from functools import reduce

import metaservlet.api as metaservlet


class LocalServerClusterManagment:
  servers_map: dict = {}
  clusters_map: dict = {}

  def __init__(self, servers, clusters):
    self.servers_map = self.make_data_map(servers)
    self.clusters_map = self.make_data_map(clusters)

  def make_data_map(self, servers: dict) -> dict:
    """
    Create a new struct of dictionary, for each register in `servers['result']` create
    a new key with the value in `label` and set the register.

    Example:
      {
        'server_label_1': { complete register server 1},
        'server_label_2': { complete register server 2},
        ...
      }
    """
    return reduce(
      lambda acc, i: {i["label"]: i, **acc},
      servers['result'],
      {}
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
