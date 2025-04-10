from metaservlet.core import call_metaservlet


def set_license_key(license_key_path: str) -> dict:
  if not license_key_path:
    raise Exception('License key path can not be empty.')
  request_params = {'licenseKeyPath': license_key_path}
  return call_metaservlet('setLicenseKey', request_params)
