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
  # artifact repository
  "config_esbconductor_repo_url_type": '22',
  "config_esbconductor_nexus3_url_label": '32',
  "config_esbconductor_nexus3_url_username": '33',
  "config_esbconductor_nexus3_url_password": '34',
  "config_esbpublisher_nexus3_release": '35',
  "config_esbpublisher_nexus3_snapshot": '36',
  "config_esbpublisher_nexus3_group": '37',
  # ldap
  "config_ldap_useLDAPAutentication": '66',
  "config_ldap_enableLDAPS": '67',
  "config_ldap_enableReferral": '68',
  "config_ldap_host": '69',
  "config_ldap_port": '70',
  "config_ldap_principalDNPrefix": '71',
  "config_ldap_adminPassword": '72',
  "config_ldap_loginField": '73',
  "config_ldap_emailField": '74',
  "config_ldap_firstName": '75',
  "config_ldap_lastName": '76',
  # job conductor
  "config_scheduler_archiveAndExecutionLogsPath": '59',
  "config_scheduler_recoveryLogsPath": '60',
  "config_scheduler_cleaning_maxOldExecutionsLogs": '61',
  "config_scheduler_cleaning_maxDurationBeforeCleaningOldExecutionsLogs": '62',
  "config_scheduler_cleaning_maxOldJobs": '63',
  "config_scheduler_cleaning_maxDurationBeforeCleaningOldJobs": '64',
  #Logs
  "config_log4j_talendAppender": '80',
  "config_log4j_talendAppender_threshold": '81',
  "config_log4j_files_option": '82',
  "config_log4j_filesize": '83',
  "config_log4j_filelimit": '84',
  "config_businessLog_path": '86',
  "config_businessLog_option": '88',
  "config_businessLog_filesize": '91',
  "config_businessLog_filelimit": '93',
  "config_keyRotationLog_path": '87',
  "config_keyRotationLog_option": '89',
  "config_keyRotationLog_filesize": '90',
  "config_keyRotationLog_filelimit": '92',
  #smtp
  "config_smtp_useSmtp": '100',
  "config_smtp_host": '101',
  "config_smtp_port": '102',
  "config_smtp_requireTLS": '103',
  "config_smtp_requireSSL": '104',
  "config_smtp_userName": '105',
  "config_smtp_password": '106',
  "config_smtp_fromAddress": '107',
  # sso
  "config_sso_useSSOLogin": '167',
  "config_sso_spEntityId": '169',
  "config_sso_idpPlugin_dropDown": '170',
  "config_sso_spLoginUrl": '171',
  "config_sso_use_mapping": '172',
  "config_sso_logout_redirect_url": '219',
  # software update
  "config_softwareupdate_localRepo_nexus3_password": '121',
  "config_softwareupdate_localRepo_nexus3_password_reader": '123',
}

sso_password = None

def settings_update_field(field: str, value: str, sso=False):
  """field: str=ssection.field
     value: str
     sso: bool True if the login change to Single Sign On """

  global sso_password
  try:
    id_field = TAC_FIELDS[field]
  except KeyError:
    raise Exception(f"The field: {field} is not found in TAC support fields")

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
