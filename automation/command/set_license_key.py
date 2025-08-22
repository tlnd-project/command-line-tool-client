import os

from metaservlet.api import set_license_key
from utilities.bitbucket_files_management import BitbucketFileManager
from settings.credentials import (
    BITBUCKET_DATA_SOURCE_URL,
    BITBUCKET_DATA_SOURCE_BRANCH,
    BITBUCKET_DATA_SOURCE_TOKEN
  )
from settings.constant import PATH_CACHE_DIRECTORY


def process_item(new_license: list):

  client_bitbucket = BitbucketFileManager(
    url=BITBUCKET_DATA_SOURCE_URL,
    branch=BITBUCKET_DATA_SOURCE_BRANCH,
    auth_token=BITBUCKET_DATA_SOURCE_TOKEN
  )
  client_bitbucket.download_file(
    name_file=new_license[0],
    full_name_file=new_license[0],
    output_path_file=PATH_CACHE_DIRECTORY
  )
  set_license_key(f'{os.getcwd()}/{new_license[0]}')
