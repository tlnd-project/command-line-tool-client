import metaservlet.api as metaservlet

from automation.tools.local_server_cluster_managment import local_storage
from settings.logger_config import logging


logger = logging.getLogger(__name__)


# TODO: change server:list for positional variables.
def process_item(server: list):
  # TODO: fail if the virtual_name is a part of the default list of the TAC. for example
  """server: server_name|virtual_server_name|match_flag
  examples:
    name_server|virtual_server_name|match_flag|host
    # delete the server, fail if it is linked a some virtual server
    example|||host_domain
    # delete the server, delete related if it is part of a virtual server
    example||f|host_domain
    # delete the virtual server, fail if it has server linked
    |virtual_example||host_domain
    # delete the virtual server, delete the relations if it has server linked
    |virtual_example|f|host_domain
    # delete the relation with the virtual server
    example|virtual_example||host_domain      <= fail if no exist? and also remove server and virtual server?
    # delete all: the server, the virtual server, the relation regardless of whether if it has other relations
    example|virtual_example|f|host_domain
  """

  server_name, cluster_name, match_flag = server
  id_server = None
  id_cluster = None
  # first, evaluate the structure of the parameters
  if server_name:
    try:
      server_register = local_storage.servers_map[server_name]
      id_server = server_register["id"]
    except KeyError:
      if match_flag != 'f':
        raise Exception(f'No such server {server_name} for remove')

  if cluster_name:
    try:
      cluster_register = local_storage.clusters_map[cluster_name]
      id_cluster = cluster_register["id"]
    except KeyError:
      raise Exception(f'No such virtual server {cluster_name} for remove')

  if (
    match_flag == 'f'
    and (id_server is None and id_cluster is None)
  ):
    raise Exception(
      'If you use `f` is necessary put the server name or virtual server name'
    )

  if match_flag == 'f':
    if id_server and id_cluster:
      logger.info(f'[REMOVE SERVER CLUSTER] force remove all')
      servers = local_storage.get_servers_from_clusters(cluster_name)
      metaservlet.remove_servers_from_virtual_server(
        [{'serverId': item['serverId']} for item in servers],
        str(id_cluster)
      )
      metaservlet.remove_virtual_server(id_cluster)
      local_storage.remove_cluster(cluster_name)

      virtual_servers = local_storage.get_virtual_servers()
      for cluster in virtual_servers:
        if local_storage.exist_server_in_cluster(server_name, cluster["label"]):
          metaservlet.remove_servers_from_virtual_server(
            [
              {'serverId': str(id_server)}
            ],
            str(cluster["id"])
          )
          local_storage.remove_linked_server(cluster["label"], server_name)
      metaservlet.remove_server(id_server)
      local_storage.remove_server(server_name)

    elif id_server and id_cluster is None:
      logger.info(f'[REMOVE SERVER CLUSTER] force remove the server')
      virtual_servers = local_storage.get_virtual_servers()
      for cluster in virtual_servers:
        if local_storage.exist_server_in_cluster(server_name, cluster["label"]):
          metaservlet.remove_servers_from_virtual_server(
            [
              {'serverId': str(id_server)}
            ],
            str(cluster["id"])
          )
          local_storage.remove_linked_server(cluster["label"], server_name)
      metaservlet.remove_server(id_server)
      local_storage.remove_server(server_name)
    elif id_server is None and id_cluster:
      logger.info(f'[REMOVE SERVER CLUSTER] force remove the virtual server')
      servers = local_storage.get_servers_from_clusters(cluster_name),
      metaservlet.remove_servers_from_virtual_server(
        [{'serverId': item['serverId']} for item in servers],
        str(id_cluster)
      )
      metaservlet.remove_virtual_server(id_cluster)
      local_storage.remove_cluster(cluster_name)
  else:

    if id_server and id_cluster:
      logger.info(f'[REMOVE SERVER CLUSTER] remove the server and the virtual server')
      if local_storage.exist_server_in_cluster(server_name, cluster_name):
        metaservlet.remove_servers_from_virtual_server(
          [
            {'serverId': str(id_server)}
          ],
          str(id_cluster)
        )
        local_storage.remove_linked_server(cluster_name, server_name)
      else:
        raise Exception(f'No such virtual server {cluster_name} for remove')

    else:
      if id_server:
        logger.info(f'[REMOVE SERVER CLUSTER] remove the server')
        if local_storage.exist_server_in_cluster(server_name):
          raise Exception(f'The server {server_name} belongs to another cluster')
        else:
          metaservlet.remove_server(id_server)
          local_storage.remove_server(server_name)

      if id_cluster:
        logger.info(f'[REMOVE SERVER CLUSTER] remove the virtual server')
        if local_storage.cluster_has_servers(cluster_name):
          raise Exception(f'The virtual server {cluster_name} has other servers linked')
        else:
          metaservlet.remove_virtual_server(id_cluster)
          local_storage.remove_cluster(cluster_name)
