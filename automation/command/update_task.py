from metaservlet.api import task_exist, update_task
from utilities.encryption import decrypt

def process_item(task: list):
  job_name, context_name, value, is_encrypted = task
  task_id = task_exist(job_name)
  if not task_id:
    raise Exception(f'A task called "{task_id}" does not exist')

  if is_encrypted=='true':
    value = decrypt(value)

  update_task(task_id, context_name, value)
