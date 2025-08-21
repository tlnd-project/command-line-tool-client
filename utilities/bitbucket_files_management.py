import pandas as pd
import requests
import urllib3, os
from io import StringIO

from settings.logger_config import logging


logger = logging.getLogger(__name__)


class BitbucketFileManager:

  def __init__(self, url: str, branch: str, auth_token: str) -> None:
    self.base_url = url.rstrip('/')
    self.branch = branch
    self.auth_token = auth_token

  def _build_file_url(self, file_name: str) -> str:
    return self.base_url.format( file_name, self.branch)

  def _get_headers(self) -> dict:
    return { "Authorization": f"Bearer {self.auth_token}" }

  def download_body_content(self, file_name: str) -> str:
    """return the text of the body request."""
    urllib3.disable_warnings()
    response = requests.get(
      self._build_file_url(file_name),
      headers=self._get_headers(),
      allow_redirects=False
    )
    response.raise_for_status()
    return response.text

  def download_file(self, file_name: str, path_file: str, force: bool = True) -> str:
    local_file = os.path.join(path_file, file_name)
    if force and os.path.exists(local_file):
      os.remove(local_file)
    if not os.path.exists(local_file):
      content = self.download_body_content(file_name)
      with open(local_file, "w") as f:
        f.write(content)
    return local_file

  def list_csv_file_rows(self, file_name: str, separator: str = '|') -> list:
    text = self.download_body_content(file_name)
    csv_dataframe = pd.read_csv(
      StringIO(text),
      sep=separator,
      header=None,
      error_bad_lines=False
    )
    return csv_dataframe.iloc[1:].reset_index(drop=True).fillna('').values.tolist()
