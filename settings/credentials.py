import os
from dotenv import load_dotenv, find_dotenv 
from utilities.encryption import decrypt


load_dotenv(find_dotenv())


WORKING_DIRECTORY = os.environ.get('WORKING_DIRECTORY')
JAR_DECRYPTION_PATH = f'{WORKING_DIRECTORY}/dtcc.jar'
CURRENT_HOST_NAME = os.environ.get('CURRENT_HOST_NAME')
TALEND_URL = os.environ.get('TALEND_URL')
TALEND_USER = os.environ.get('TALEND_USER')
TALEND_PASSWORD = decrypt(
  os.environ.get('TALEND_PASSWORD'),
  f'{WORKING_DIRECTORY}/settings/dtcc_master.key',
  JAR_DECRYPTION_PATH,
)
#TALEND_PASSWORD = os.environ.get('TALEND_PASSWORD')
METASERVLET_CALLER = os.environ.get('METASERVLET_CALLER')
BITBUCKET_AUTH_TOKEN = os.environ.get('BITBUCKET_AUTH_TOKEN')
BITBUCKET_REPO_URL = os.environ.get('BITBUCKET_REPO_URL')
ENVIRONMENT_FLAG = os.environ.get('ENVIRONMENT_FLAG')
