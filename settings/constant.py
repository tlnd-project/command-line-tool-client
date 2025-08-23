import os
import socket


__all__ = [
  "ENV_KEYS_NAME",
  "ENV_NAME",
  "NAME_DTCC_JAR",
  "NAME_DIRECTORY_CACHE",
  "NAME_DTCC_KEY",
  "NAME_DTCC_KEY_MASTER",
  "NAME_DTCC_KEY_BITBUCKET",
  "CURRENT_HOST_NAME",
  "WORKING_DIRECTORY",
  "PATH_CACHE_DIRECTORY",
  "PATH_FILE_DTCC_JAR",
  "PATH_FILE_ENV",
  "PATH_FILE_KEYS_ENV",
  "PATH_FILE_KEY_BITBUCKET",
  "ENVIRONMENT_FLAG"
]

# set the name of the files
ENV_KEYS_NAME = '.env_keys'
ENV_NAME = '.env'
NAME_DTCC_JAR = 'dtcc.jar'
NAME_DIRECTORY_CACHE = '.cache'
NAME_DTCC_KEY = 'dtcc.key'
NAME_DTCC_KEY_MASTER = 'dtcc_master.key'
NAME_DTCC_KEY_BITBUCKET = 'dtcc_bbk.key'

_SERVER_DEV = 'satacd'
_SERVER_QA = 'satacq'
_SERVER_PS = 'satacu'
_SERVER_PROD = 'satacp'

CURRENT_HOST_NAME = socket.gethostname()
WORKING_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_CACHE_DIRECTORY = os.path.join(WORKING_DIRECTORY, NAME_DIRECTORY_CACHE)
PATH_FILE_DTCC_JAR = f'{WORKING_DIRECTORY}/{NAME_DTCC_JAR}'
PATH_FILE_ENV = f'{PATH_CACHE_DIRECTORY}/{ENV_NAME}'
PATH_FILE_KEYS_ENV = f'{PATH_CACHE_DIRECTORY}/{ENV_KEYS_NAME}'
PATH_FILE_KEY_BITBUCKET = f'{PATH_CACHE_DIRECTORY}/{NAME_DTCC_KEY_BITBUCKET}'


def get_flag_environment():
  if _SERVER_DEV in CURRENT_HOST_NAME:
    return "DEV"
  elif _SERVER_QA in CURRENT_HOST_NAME:
    return "QA"
  elif _SERVER_PS in CURRENT_HOST_NAME:
    return "PSE"
  elif _SERVER_PROD in CURRENT_HOST_NAME:
    return "PROD"
  return None

ENVIRONMENT_FLAG = get_flag_environment()
