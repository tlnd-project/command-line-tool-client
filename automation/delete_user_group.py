from metaservlet.api import user_group_exist, delete_user_group

def main(user_groups: list):
  for user_group in user_groups:
    print('-----', user_group)
    user_group_name = user_group[0]
    try:
      user_group_id = user_group_exist(user_group_name)
      if not user_group_id:
        raise Exception(f'A user group called "{user_group_name}" does not exist')
      delete_user_group(user_group_name)
    except Exception as e:
      print('ERROR: ', e.args)
      continue
