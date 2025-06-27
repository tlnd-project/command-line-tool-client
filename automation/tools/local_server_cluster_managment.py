from collections.abc import Callable
from functools import reduce
from typing import Optional

import metaservlet.api as metaservlet
from settings.logger_config import logging


logger = logging.getLogger(__name__)


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

  def exist_server_in_cluster(self, server_name: str, cluster_name: Optional[str] = None) -> bool:
    if cluster_name is not None:
      list_cluster = {cluster_name: self.clusters_map[cluster_name]}
    else:
      list_cluster = self.clusters_map

    for key, cluster in list_cluster.items():
      for server in cluster.get('servers', []):
        if server_name == server["serverLabel"]: return True
    return False

  def cluster_has_servers(self, cluster_server_name: str) -> bool:
    return len(self.clusters_map[cluster_server_name].get('servers', [])) > 0

  def add_server_to_cluster(self, server_name: int, cluster_name: str):
    cluster = self.clusters_map[cluster_name]
    if not 'servers' in cluster: cluster['servers'] = []
    server_item = self.servers_map[server_name]
    cluster['servers'].append(
      {'serverId': server_item['id'], 'serverLabel': server_item['label']}
    )

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

  def remove_server(self, server_name: str) -> None:
    del self.servers_map[server_name]

  def remove_cluster(self, cluster_name: str) -> None:
    del self.clusters_map[cluster_name]

  def remove_linked_server(self, cluster_name: str, server_name: str) -> None:
    server_item = {
      "serverId": self.servers_map[server_name]["id"],
      "serverLabel": self.servers_map[server_name]["label"]
    }
    if "servers" not in self.clusters_map[cluster_name]:
      raise Exception(f"Cluster {cluster_name} has no servers")
    self.clusters_map[cluster_name]["servers"].remove(server_item)

  def get_servers_from_clusters(self, cluster_name: str) -> list:
    return self.clusters_map[cluster_name].get('servers', [])

  def get_virtual_servers(self) -> list:
    return [cluster for cluster_name, cluster in self.clusters_map.items()]

local_storage = LocalServerClusterManagment(
  metaservlet.list_server(),
  metaservlet.list_virtual_servers()
)
