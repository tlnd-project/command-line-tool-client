from metaservlet.api import task_exist, update_task


def process_item(task: list):
  job_name, jvm_value = task
  task_id = task_exist(job_name)
  if not task_id:
    raise Exception(f'A task called "{task_id}" does not exist')

  update_task(task_id, context_name, value)
