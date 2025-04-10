from metaservlet.core import call_metaservlet


def user_exists(user_name: str) -> bool:
  if not user_name:
    raise Exception('User name can not be empty.')
  request_params = {'userLogin': user_name}
  response = call_metaservlet('userExist' , request_params)
  return response['result']


def delete_user(user_name: str) -> dict:
  if not user_name:
    raise Exception('User name can not be empty.')
  request_params = {'userLogin': user_name}
  return call_metaservlet('deleteUser', request_params)


def user_group_exist(user_group_name: str) -> int:
  if not user_group_name:
    raise Exception('User group name can not be empty.')
  request_params = {'label': user_group_name}
  response = call_metaservlet('getIdByUserGroupName', request_params)
  return response.get("id", 0)


def create_user_group(
  user_group_name: str, description: str, type:str='DQ'
) -> dict:
  if not user_group_name:
    raise Exception('User group name can not be empty.')
  request_params = {
    'label': user_group_name, 'type': type, 'description': description,
  }
  return call_metaservlet('createUserGroup', request_params)


def delete_user_group(user_group_id: int) -> dict:
  request_params = {'id': user_group_id}
  return call_metaservlet('deleteUserGroupById', request_params)
