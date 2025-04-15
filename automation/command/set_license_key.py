from metaservlet.api import set_license_key
from utilities.bitbucket_files_management import download_file
import os


def process_item(license: list):
  download_file(license[0])
  set_license_key(f'{os.getcwd()}/{license[0]}')
