from metaservlet.api import create_user_group, user_group_exist


def process_item(user_group: list):
  user_group_name, description = user_group

  if user_group_exist(user_group_name):
    raise Exception(f'A user group called "{user_group_name}" already exist')
  create_user_group(user_group_name, description)
