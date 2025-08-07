from metaservlet.core import call_metaservlet
import settings.credentials as env
from settings.logger_config import logging


logger = logging.getLogger(__name__)


def test_get_info_user():
  # Get info user with the command metaservlet
  request_params = {
    'userLogin': env.TALEND_USER,
  }
  call_metaservlet('getUserInfo', request_params)
