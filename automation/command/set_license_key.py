import os

from metaservlet.api import set_license_key
from utilities.bitbucket_files_management import get_client_bitbucket
from settings.constant import path_cache_directory


def process_item(new_license: list):
  client_bitbucket = get_client_bitbucket()
  client_bitbucket.download_file(
    file_name=new_license[0],
    path_file=path_cache_directory
  )
  set_license_key(f'{os.getcwd()}/{new_license[0]}')
