import metaservlet.api as metaservlet

from automation.command import local_storage


# TODO: change server:list for positional variables.
def process_item(server: list):
  """server: server_name|virtual_server_name|match_flag
  examples:
    name_server||
  """
  server_name, virtual_server_name, match_flag = server
  id_server = None
  id_virtual_server = None

  # first, evaluate the structure of the parameters
  if server_name:
    try:
      server_register = local_storage.servers_map[server_name]
      id_server = server_register["id"]
    except KeyError:
      raise Exception(f'No such server {server_name} for remove')

  if virtual_server_name:
    try:
      virtual_server_register = local_storage.clusters_map[virtual_server_name]
      id_virtual_server = virtual_server_register["id"]
    except KeyError:
      raise Exception(f'No such virtual server {virtual_server_name} for remove')

  # if match_flag == '1' then exist `server_name` and `virtual_server_name`
  if (
    match_flag == '1'
    and (id_server is None or id_virtual_server is None)
  ):
      raise Exception(f'No such server {server_name} for remove')

  # if match_flag == '1' first remove the relation, then remove the `virtual_server`
  # and finally remove the server
  if (
    match_flag == '1'
    and local_storage.exist_server_in_cluster(id_server, virtual_server_name)
  ):
    metaservlet.remove_servers_from_virtual_server(
      [
        {'serverId': str(id_server)}
      ],
      str(id_virtual_server)
    )
    metaservlet.remove_virtual_server(id_virtual_server)
    metaservlet.remove_server(id_server)

  else:
    # remove the server, the virtual_server or both
    if virtual_server_name:
      metaservlet.remove_virtual_server(id_virtual_server)

    if server_name:
      metaservlet.remove_server(id_server)
