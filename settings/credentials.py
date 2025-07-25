import os
import socket
from dotenv import load_dotenv, find_dotenv
from utilities.encryption import decrypt


load_dotenv(find_dotenv())


WORKING_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAR_DECRYPTION_PATH = f'{WORKING_DIRECTORY}/dtcc.jar'
CURRENT_HOST_NAME = socket.gethostname()
TALEND_URL = os.environ.get('TALEND_URL')
TALEND_USER = os.environ.get('TALEND_USER')
if os.environ.get("IS_PASSWORD_ENCRYPTED")=="1":
  TALEND_PASSWORD = decrypt(
    os.environ.get('TALEND_PASSWORD'),
    f'{WORKING_DIRECTORY}/settings/dtcc_master.key',
    JAR_DECRYPTION_PATH,
  )
else:
  TALEND_PASSWORD = os.environ.get('TALEND_PASSWORD')
METASERVLET_CALLER = os.environ.get('METASERVLET_CALLER')
BITBUCKET_AUTH_TOKEN = decrypt(
    os.environ.get('BITBUCKET_AUTH_TOKEN'),
    f'{WORKING_DIRECTORY}/settings/dtcc_bbk.key',
    JAR_DECRYPTION_PATH,
)
BITBUCKET_REPO_BRANCH = os.environ.get('BITBUCKET_REPO_BRANCH')
BITBUCKET_REPO_URL = os.environ.get('BITBUCKET_REPO_URL')
ENVIRONMENT_FLAG = os.environ.get('ENVIRONMENT_FLAG')

TALEND_SCRAPPER_SSO_FLAG = os.environ.get('TALEND_SCRAPPER_SSO_FLAG')
TALEND_SCRAPPER_SSO_URL = os.environ.get('TALEND_SCRAPPER_SSO_URL')
TALEND_SCRAPPER_SSO_USER = os.environ.get('TALEND_SCRAPPER_SSO_USER')

# one password if the SSO login.
TALEND_SCRAPPER_SSO_DOMAIN = os.environ.get('TALEND_SCRAPPER_SSO_DOMAIN')
TALEND_SCRAPPER_SSO_PATH_COMMAND = os.environ.get('TALEND_SCRAPPER_SSO_PATH_COMMAND')
TALEND_SCRAPPER_SSO_CONF_INI = os.environ.get('TALEND_SCRAPPER_SSO_CONF_INI')

MANIFEST_PATH = os.environ.get('MANIFEST_PATH')
LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO")
LOG_NAME = os.environ.get('LOG_NAME', "command.log")
