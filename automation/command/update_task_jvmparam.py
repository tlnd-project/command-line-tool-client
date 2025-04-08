from metaservlet.api import task_exist, list_task_params, add_task_jvmparam


def process_item(task: list):
  job_name, jvm_value = task
  task_id = task_exist(job_name)
  if not task_id:
    raise Exception(f'A task called "{task_id}" does not exist')
  jvmTaskList = list_task_params(task_id)
  if not jvmTaskList["result"]:
    add_task_jvmparam(task_id, jvm_value)
  else:
    ""
#  update_task(task_id, context_name, value)
