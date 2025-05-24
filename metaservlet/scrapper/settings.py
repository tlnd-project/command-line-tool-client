import ast

from metaservlet.core import TACHttpClient, TACHttpClientSSO
from .get_function_token import get_function_tokens
from settings.credentials import TALEND_USER, TALEND_PASSWORD, TALEND_SCRAPPER_SSO_FLAG

TAC_FIELDS = {
  "artifact_repository": {
    "password": 34
  },
  "software_update": {
    "local_deployment_password": 121,
    "local_reader_password": 123
  },
  "ldap": {
    "admin_password": 72
  },
  "smtp": {
    "from_address": 107
  }
}
function_tokens = get_function_tokens()


def settings_update_field(field, value, sso=False):
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
  if TALEND_SCRAPPER_SSO_FLAG:
    _tmp_client = TACHttpClientSSO(base_url=env.TALEND_SCRAPPER_URL)
    tac_client = _tmp_client.login(
      username=env.TALEND_SCRAPPER_USER,
      password=env.TALEND_SCRAPPER_PASSWORD
    )
  else:
    tac_client = TACHttpClient(base_url=env.TALEND_URL)
    tac_client.login(
      username=env.TALEND_USER,
      password=env.TALEND_PASSWORD
    )

  # 2) set xsrf_token
  tac_client.get_xsrf_token()
  # 3) update field
  tac_client.configuration_update_field(id_field, value)
  # 4) logout
  tac_client.logout()
