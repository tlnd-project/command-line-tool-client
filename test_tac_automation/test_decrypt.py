import os

from utilities.encryption import decrypt
from settings.credentials import (
  JAR_DECRYPTION_PATH, WORKING_DIRECTORY
)
from settings.logger_config import logging


logger = logging.getLogger(__name__)


def test_decrypt_talend_password():
  if os.environ.get("IS_PASSWORD_ENCRYPTED")=="1":
    decrypt(
      os.environ.get('TALEND_PASSWORD'),
      f'{WORKING_DIRECTORY}/settings/dtcc_master.key',
      JAR_DECRYPTION_PATH,
    )
  else:
    os.environ.get('TALEND_PASSWORD')

def test_decrypt_bitbucket():
  decrypt(
      os.environ.get('BITBUCKET_AUTH_TOKEN'),
      f'{WORKING_DIRECTORY}/settings/dtcc_bbk.key',
      JAR_DECRYPTION_PATH,
  )
