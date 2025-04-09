import pandas as pd
import requests
import urllib3
from io import StringIO
from settings.credentials import (
  BITBUCKET_AUTH_TOKEN, BITBUCKET_REPO_URL, ENVIRONMENT_FLAG
)


urllib3.disable_warnings()


def download_file(file_url: str) -> str:
  headers = {
    'Authorization': f'Bearer {BITBUCKET_AUTH_TOKEN}'
  }
  response = requests.get(
    file_url, verify=False, allow_redirects=True, headers=headers
  )
  return response.text


def get_csv_from_bitbucket(file_url: str, separator: str=','):
  return pd.read_csv(
    StringIO(download_file(file_url)),
    sep=separator,
    header=None,
    error_bad_lines=False
  )


def build_file_url(file_name: str) -> str:
  return BITBUCKET_REPO_URL.format(f'{ENVIRONMENT_FLAG}/{file_name}')


def load_file(file_name: str) -> list:
  file_url = build_file_url(file_name)
  csv_dataframe = get_csv_from_bitbucket(file_url, '|')
  return csv_dataframe.fillna('').values.tolist()
