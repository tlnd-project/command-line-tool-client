from metaservlet.core import call_metaservlet, MetaservletException
from metaservlet.error_codes import INVALID_PARAMETER_CODE


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


def get_user_info(user_name: str) -> dict:
  if not user_name:
    raise Exception('User name can not be empty.')
  request_params = {'userLogin': user_name}
  return call_metaservlet('getUserInfo' , request_params)


def user_group_exist(user_group_name: str) -> int:
  if not user_group_name:
    raise Exception('User group name can not be empty.')
  request_params = {'label': user_group_name}
  try:
    response = call_metaservlet('getIdByUserGroupName', request_params)
    return response.get("id", 0)
  except MetaservletException as e:
    if e.args[1]==INVALID_PARAMETER_CODE:
      return 0
  # TODO: what is the default value returned?


def create_user_group(
  user_group_name: str, description: str, user_group_type: str='DQ'
) -> dict:
  if not user_group_name:
    raise Exception('User group name can not be empty.')
  request_params = {
    'label': user_group_name, 'type': user_group_type, 'description': description,
  }
  return call_metaservlet('createUserGroup', request_params)


def delete_user_group(user_group_id: int) -> dict:
  request_params = {'id': user_group_id}
  return call_metaservlet('deleteUserGroupById', request_params)


def add_user_to_user_group(user_id: int, user_group_id: int) -> dict:
  request_params = {'id': user_group_id, 'users': [{'id': user_id}]}
  return call_metaservlet('addUsersToUserGroup', request_params)


def remove_user_from_user_group(user_id: int, user_group_id: int) -> dict:
  request_params = {'id': user_group_id, 'users': [{'id': user_id}]}
  return call_metaservlet('removeUsersFromUserGroup', request_params)


def update_user(user_unique_id: str, user_name: str, user_role_list: list):
  request_params = {
    'uniqueId': user_unique_id,
    'userLogin': user_name,
    'userRole': user_role_list,
    'userType': 'DQ',
  }
  return call_metaservlet('updateUser', request_params)
