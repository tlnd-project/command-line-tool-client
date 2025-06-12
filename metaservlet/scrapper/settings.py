import ast

from metaservlet.core import TACHttpClient, TACHttpClientSSO
from utilities.sso_token import get_unique_sso_password
from settings.logger_config import logging
from settings.credentials import (
  TALEND_URL,
  TALEND_USER,
  TALEND_PASSWORD,
  TALEND_SCRAPPER_URL,
  TALEND_SCRAPPER_SSO_FLAG,
  TALEND_SCRAPPER_USER,
)


logger = logging.getLogger(__name__)

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

sso_password = None

def settings_update_field(field: str, value: str, sso=False):
  """field: str=ssection.field
     value: str
     sso: bool True if the login change to Single Sign On """

  global sso_password
  try:
    section, field_section = field.split(".")
  except IndexError:
    logger.error(
      f"[SETTINGS UPDATE] => The value: {field} is not has a format `section.field`"
    )
    raise Exception(f"The value: {field} is not has a format `section.field`")

  try:
    id_field = TAC_FIELDS[section][field_section]
  except KeyError:
    logger.error(
      f"[SETTINGS UPDATE]"
      f"=> The section.field: {field} is not found in TAC support fields"
    )
    raise Exception(f"The section.field: {field} is not found in TAC support fields")

  # 1) login
  logger.info(f"[SETTINGS UPDATE] => step 1 - LOGIN ")
  if TALEND_SCRAPPER_SSO_FLAG == "1":
    if sso_password is None:
      sso_password = get_unique_sso_password()

    _tmp_client = TACHttpClientSSO(sso_url=TALEND_SCRAPPER_URL)
    tac_client = _tmp_client.login(
      username=TALEND_SCRAPPER_USER,
      password=sso_password
    )
  else:
    tac_client = TACHttpClient(base_url=TALEND_URL)
    tac_client.login(
      username=TALEND_USER,
      password=TALEND_PASSWORD
    )

  # TODO: add validate login
  # 2) set xsrf_token
  logger.info(f"[SETTINGS UPDATE] => step 2 - XSRF_TOKEN")
  tac_client.get_xsrf_token()
  # 3) update field
  logger.info(f"[SETTINGS UPDATE] => step 3 - UPDATE FIELD")
  tac_client.configuration_update_field(id_field, value)
  # 4) logout
  logger.info(f"[SETTINGS UPDATE] => step 4 - LOGOUT")
  tac_client.logout()
