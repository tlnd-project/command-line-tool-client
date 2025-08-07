from metaservlet.scrapper.settings import TAC_FIELDS
from utilities.sso_token import get_unique_sso_password
from metaservlet.core import TACHttpClient, TACHttpClientSSO
from settings.credentials import (
  TALEND_URL,
  TALEND_USER,
  TALEND_PASSWORD,
  TALEND_SCRAPPER_SSO_URL,
  TALEND_SCRAPPER_SSO_FLAG,
  TALEND_SCRAPPER_SSO_USER,
)
from settings.logger_config import logging


logger = logging.getLogger(__name__)


def test_login_logout():
  # 1) login
  logger.info(f"[TEST test_login_logout] => step 1 - LOGIN ")
  if TALEND_SCRAPPER_SSO_FLAG == "1":
    sso_password = get_unique_sso_password()
    _tmp_client = TACHttpClientSSO(sso_url=TALEND_SCRAPPER_SSO_URL)
    tac_client = _tmp_client.login(
      username=TALEND_SCRAPPER_SSO_USER,
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
  logger.info(f"[TEST test_login_logout] => step 2 - XSRF_TOKEN")
  tac_client.get_xsrf_token()

  # 4) logout
  logger.info(f"[TEST test_login_logout] => step 4 - LOGOUT")
  tac_client.logout()
