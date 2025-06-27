import metaservlet.api as metaservlet

from automation.tools.local_server_cluster_managment import local_storage


# TODO: change server:list for positional variables.
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
    # TODO: whats is the server_id and cluster_id default values. these variables is set inside the block if.
    metaservlet.add_server_to_virtual_server(server_id, cluster_id)
    local_storage.add_server_to_cluster(server_name, cluster_name)
