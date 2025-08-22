import pandas as pd
import requests
import urllib3, os
from io import StringIO


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
      allow_redirects=False,
      verify=False
    )
    response.raise_for_status()
    return response.text

  def download_file(self, name_file: str, full_name_file: str, output_path_file: str, force: bool = True) -> str:
    local_file = os.path.join(output_path_file, name_file)
    if force and os.path.exists(local_file):
      os.remove(local_file)
    if not os.path.exists(local_file):
      content = self.download_body_content(full_name_file)
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
