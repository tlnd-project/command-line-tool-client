from utilities.bitbucket_files_management import BitbucketFileManager
from settings.logger_config import logging
from settings.credentials import (
    BITBUCKET_DATA_SOURCE_URL,
    BITBUCKET_DATA_SOURCE_BRANCH,
    BITBUCKET_DATA_SOURCE_TOKEN,
    ENVIRONMENT_FLAG
  )


logger = logging.getLogger(__name__)


def test_download_file():
  client_bitbucket = BitbucketFileManager(
    url=BITBUCKET_DATA_SOURCE_URL,
    branch=BITBUCKET_DATA_SOURCE_BRANCH,
    auth_token=BITBUCKET_DATA_SOURCE_TOKEN
  )
  data_list = client_bitbucket.list_csv_file_rows(
    f"{ENVIRONMENT_FLAG}/'dtcc.key'"
  )
