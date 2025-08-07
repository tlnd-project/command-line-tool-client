from settings.logger_config import logging
from test_bitbucket import test_download_file
from test_scrapper import test_login_logout
from test_metaservlet import test_get_info_user
from test_decrypt import test_decrypt_bitbucket, test_decrypt_talend_password
from test_files_csv import validate_all_txt_from_project


logger = logging.getLogger(__name__)


# validate the decrypt bitbucket token and the password of the user talend
logger.info(f"[=== > TEST DECRYPT < === ]")
test_decrypt_bitbucket()
test_decrypt_talend_password()

# test the access to bitbucket
logger.info(f"[=== > TEST BITBUCKET < === ]")
test_download_file()

# Login and logout scrapper
logger.info(f"[=== > TEST SCRAPPER < === ]")
test_login_logout()

# get info user with metaservlet command
logger.info(f"[=== > TEST METASERVLET < === ]")
test_get_info_user()

# retrieve all files CSV and validate the format.
logger.info(f"[=== > TEST FILES TXT < === ]")
validate_all_txt_from_project()