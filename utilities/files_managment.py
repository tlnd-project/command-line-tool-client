import pandas as po
import requests
from io import StringIO
from settings.credentials import BITBUCKET_AUTH_TOKEN

def get_from_bitbucket(file_url: str):
  headers = {
    'Authorization': f'Bearer {BITBUCKET_AUTH_TOKEN}'
  }
  response = requests.get(file_url, allow_redirects=True, headers=headers)
  return pd.read_csv(StringIO(response.text) , sep=',')
