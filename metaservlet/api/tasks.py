from metaservlet.core import call_metaservlet


def task_exist(task_name: str):
  if not task_name:
    raise Exception('Task name can not be empty')
  request_params = {'taskName': task_name}
  response = call_metaservlet('getTaskIdByName', request_params)
  return response.get("taskId", 0)


def update_task(task_id, context_name, value):
  if not context_name:
    raise Exception('Context name can not be empty')
  request_params = {'taskId': task_id, 'context': {f'{context_name}': value}}
  return call_metaservlet('updateTask', request_params)


def list_task_params(task_id):
  request_params = {'taskId': task_id}
  return call_metaservlet('listTaskParams', request_params)


def update_task_jvmparam(jvm_param_id: int, value, is_active: bool):
  request_params = {'id': jvm_param_id, 'jvmParam': value, "active": is_active}
  return call_metaservlet('updateTaskParam', request_params)


def add_task_jvmparam(task_id: int, value, is_active: bool):
  request_params = {'taskId': task_id, 'jvmParam': value, "active": is_active}
  return call_metaservlet('addTaskParam', request_params)


def delete_jvm_param(jvm_param_id: int):
  request_params = {'id': jvm_param_id}
  return call_metaservlet('deleteTaskParam', request_params)