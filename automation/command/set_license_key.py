from metaservlet.api import set_license_key
from utilities.files_management import download_file, build_file_url, write_file
import os


def process_item(license: list):
  license_name = license[0]
  license_url = build_file_url(license_name)
  license_content = download_file(license_url)
  write_file(license_name, license_content)
  set_license_key(f'{os.getcwd()}/{license_name}')
