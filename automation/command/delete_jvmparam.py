from metaservlet.api import task_exist, list_task_params, delete_jvm_param
from automation.command.update_task_jvmparam import find_param

                 
def process_item(jvm_param: list):
  job_name, tag_param = jvm_param

  task_id = task_exist(job_name)
  if not task_id:
    raise Exception(f'A task called "{job_name}" does not exist')

  jvm_params_list = list_task_params(task_id)
  jvm_param_id = find_param(tag_param, jvm_params_list['result'])
  if not jvm_param_id:
    raise Exception(f'A "{job_name}" task have no param called {tag_param}')
  
  delete_jvm_param(jvm_param_id)
