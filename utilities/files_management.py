import pandas as pd
import requests
from io import StringIO
from settings.credentials import BITBUCKET_AUTH_TOKEN, BITBUCKET_REPO_URL, ENVIRONMENT_FLAG


def get_csv_from_bitbucket(file_url: str, separator: str=','):
  headers = {
    'Authorization': f'Bearer {BITBUCKET_AUTH_TOKEN}'
  }
  response = requests.get(
    file_url, verify=False, allow_redirects=True, headers=headers
  )
  return pd.read_csv(StringIO(response.text) , sep=separator, header=None, error_bad_lines=False)


def build_file_url(file_name: str) -> str:
  return BITBUCKET_REPO_URL.format(f'{ENVIRONMENT_FLAG}/{file_name}')


def load_file(file_name: str) -> list:
  file_url = build_file_url(file_name)
  csv_dataframe = get_csv_from_bitbucket(file_url, '|')
  csv_dataframe.fillna(None)
  return csv_dataframe.values.tolist()
