from metaservlet.api import task_exist, list_task_params


def process_item(task: list):
  job_name, jvm_value = task
  task_id = task_exist(job_name)
  if not task_id:
    raise Exception(f'A task called "{task_id}" does not exist')
  print(list_task_params(task_id))
#  update_task(task_id, context_name, value)
