from metaservlet.api import task_exist, update_task
from utilities.bitbucket_files_management import download_file
from utilities.encryption import decrypt
from settings.credentials import JAR_DECRYPTION_PATH


KEY_NAME = 'dtcc.key'


def process_item(task: list):
  job_name, context_name, value, is_encrypted = task
 
  task_id = task_exist(job_name)
  if not task_id:
    raise Exception(f'A task called "{job_name}" does not exist')
  if is_encrypted=='true':
    key_path = download_file(KEY_NAME)
    value = decrypt(value, key_path, JAR_DECRYPTION_PATH)
  update_task(task_id, context_name, value)
