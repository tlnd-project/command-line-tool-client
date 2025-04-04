from metaservlet.api import set_license_key


def process_item(license: list):
  set_license_key(license[0])
