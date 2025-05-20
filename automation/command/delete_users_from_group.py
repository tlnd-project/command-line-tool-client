from metaservlet.api import (
    get_user_info,
    remove_user_from_user_group,
    user_exists,
    user_group_exist,
)


def process_item(item: list):
  user_name, user_group_name = item
  user_group_id = user_group_exist(user_group_name)
  if not user_group_id:
    raise Exception(f'A user group called "{user_group_name}" does not exist')
  if not user_exists(user_name):
    raise Exception(f'A user called {user_name} does not exist')
  user_id = get_user_info(user_name).get('userId')
  remove_user_from_user_group(user_id, user_group_id)
