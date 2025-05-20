import os

from metaservlet.api import set_license_key
from utilities.bitbucket_files_management import download_file


def process_item(new_license: list):
  download_file(new_license[0])
  set_license_key(f'{os.getcwd()}/{new_license[0]}')
