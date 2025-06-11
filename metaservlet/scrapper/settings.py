import ast

from metaservlet.core import TACHttpClient, TACHttpClientSSO
from settings.credentials import (
  TALEND_URL,
  TALEND_USER,
  TALEND_PASSWORD,
  TALEND_SCRAPPER_URL,
  TALEND_SCRAPPER_SSO_FLAG,
  TALEND_SCRAPPER_USER,
  TALEND_SCRAPPER_PASSWORD,
)

TAC_FIELDS = {
  "artifact_repository": {
    "password": '34',
  },
  "software_update": {
    "local_deployment_password": '121',
    "local_reader_password": '123',
  },
  "ldap": {
    "admin_password": '72',
  },
  "smtp": {
    "from_address": '107',
  }
}


def settings_update_field(field: str, value: str, sso=False):
  """field: str=ssection.field
     value: str
     sso: bool True if the login change to Single Sign On """

  try:
    section, field_section = field.split(".")
  except IndexError:
    raise Exception(f"The value: {field} is not has a format `section.field`")

  try:
    id_field = TAC_FIELDS[section][field_section]
  except KeyError:
    raise Exception(f"The section.field: {field} is not found in TAC support fields")

  # 1) login
  if TALEND_SCRAPPER_SSO_FLAG == "1":
    _tmp_client = TACHttpClientSSO(sso_url=TALEND_SCRAPPER_URL)
    tac_client = _tmp_client.login(
      username=TALEND_SCRAPPER_USER,
      password=TALEND_SCRAPPER_PASSWORD
    )
  else:
    tac_client = TACHttpClient(base_url=TALEND_URL)
    tac_client.login(
      username=TALEND_USER,
      password=TALEND_PASSWORD
    )


  # TODO: add validate login
  # 2) set xsrf_token
  tac_client.get_xsrf_token()
  # 3) update field
  tac_client.configuration_update_field(id_field, value)
  # 4) logout
  tac_client.logout()
