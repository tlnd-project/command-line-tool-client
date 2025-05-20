from metaservlet.api import delete_user_group, user_group_exist


def process_item(user_group: list):
  user_group_id = user_group_exist(user_group[0])
  if not user_group_id:
    raise Exception(f'A user group called "{user_group[0]}" does not exist')
  delete_user_group(user_group_id)
