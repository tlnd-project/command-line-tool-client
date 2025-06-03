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
BITBUCKET_AUTH_TOKEN = os.environ.get('BITBUCKET_AUTH_TOKEN')
BITBUCKET_REPO_BRANCH = os.environ.get('BITBUCKET_REPO_BRANCH')
BITBUCKET_REPO_URL = os.environ.get('BITBUCKET_REPO_URL')
ENVIRONMENT_FLAG = os.environ.get('ENVIRONMENT_FLAG')
TALEND_SCRAPPER_SSO_FLAG = os.environ.get('TALEND_SCRAPPER_SSO_FLAG')
TALEND_SCRAPPER_URL = os.environ.get('TALEND_SCRAPPER_URL')
TALEND_SCRAPPER_USER = os.environ.get('TALEND_SCRAPPER_USER')
if os.environ.get("IS_TALEND_SCRAPPER_PASSWORD_ENCRYPTED")=="1":
  TALEND_SCRAPPER_PASSWORD = decrypt(
    os.environ.get('TALEND_SCRAPPER_PASSWORD'),
    f'{WORKING_DIRECTORY}/settings/sso_talend.key',
    JAR_DECRYPTION_PATH,
  )
else:
  TALEND_SCRAPPER_PASSWORD = os.environ.get('TALEND_SCRAPPER_PASSWORD')
TALEND_SCRAPPER_DOMAIN = os.environ.get('TALEND_SCRAPPER_DOMAIN')
TALEND_SCRAPPER_PATH_COMMAND = os.environ.get('TALEND_SCRAPPER_PATH_COMMAND')
TALEND_SCRAPPER_CONF_INI = os.environ.get('TALEND_SCRAPPER_CONF_INI')


MANIFEST_PATH = os.environ.get('MANIFEST_PATH')
LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO")
LOG_NAME = os.environ.get('LOG_NAME', "command.log")
