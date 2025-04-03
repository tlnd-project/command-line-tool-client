import os
from dotenv import load_dotenv, find_dotenv 

load_dotenv(find_dotenv())

TALEND_URL = os.environ.get('TALEND_URL')
TALEND_USER = os.environ.get('TALEND_USER')
TALEND_PASSWORD = os.environ.get ('TALEND_PASSWORD')
METASERVLET_CALLER = os.environ.get('METASERVLET_CALLER')
BITBUCKET_AUTH_TOKEN = os.environ.get('BITBUCKET_AUTH_TOKEN')
BITBUCKET_REPO_URL = os.environ.get('BITBUCKET_REPO_URL')
ENVIRONMENT_FLAG = os.environ.get('ENVIRONMENT_FLAG')
