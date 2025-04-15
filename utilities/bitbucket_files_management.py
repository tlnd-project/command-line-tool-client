import pandas as pd
import requests
import urllib3, os
from io import StringIO
from settings.credentials import (
  BITBUCKET_AUTH_TOKEN, BITBUCKET_REPO_URL, ENVIRONMENT_FLAG
)


urllib3.disable_warnings()


def build_file_url(file_name: str) -> str:
  return BITBUCKET_REPO_URL.format(f'{ENVIRONMENT_FLAG}/{file_name}')


def download_file_content(file_name: str) -> str:
  file_url = build_file_url(file_name)
  headers = {
    'Authorization': f'Bearer {BITBUCKET_AUTH_TOKEN}'
  }
  response = requests.get(
    file_url, verify=False, allow_redirects=True, headers=headers
  )
  return response.text


def write_file(file_name, file_content):
  with open(f'./{file_name}', 'w') as file:
    file.write(file_content)


def download_file(file_name: str):
  if os.path.isfile(f'./{file_name}'):
    return
  write_file(download_file_content(file_name))


def load_csv_from_bitbucket(file_name: str, separator: str=','):
  return pd.read_csv(
    StringIO(download_file_content(file_name)),
    sep=separator,
    header=None,
    error_bad_lines=False
  )


def list_csv_file_rows(file_name: str) -> list:
  csv_dataframe = load_csv_from_bitbucket(file_name, '|')
  return csv_dataframe.iloc[1:].reset_index(drop=True).fillna('').values.tolist()

