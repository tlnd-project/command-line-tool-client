from metaservlet.api import task_exist, list_task_params, add_task_jvmparam, update_task_jvmparam


def find_param(tag_param: str, jvm_params_list: list) -> int:
  for jvm_param in jvm_params_list:
    if jvm_param.get('description', "")==tag_param:
      return jvm_param['id']
  return 0

                 
def process_item(task: list):
  job_name, tag_param, jvm_value, is_active_flag = task
  task_id = task_exist(job_name)

  if not task_id:
    raise Exception(f'A task called "{job_name}" does not exist')

  jvm_params_list = list_task_params(task_id)
  jvm_param_id = find_param(tag_param, jvm_params_list['result'])

  if not jvm_param_id:
    add_task_jvmparam(task_id, jvm_value, tag_param, is_active_flag=='true')
  else:
    update_task_jvmparam(jvm_param_id, jvm_value, is_active_flag=='true')
