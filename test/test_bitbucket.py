from utilities.bitbucket_files_management import download_file
from settings.logger_config import logging


logger = logging.getLogger(__name__)


def test_download_file():
  KEY_NAME = 'dtcc.key'
  download_file(KEY_NAME)
