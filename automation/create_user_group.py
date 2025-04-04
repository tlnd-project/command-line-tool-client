from metaservlet.api import user_group_exist, create_user_group

def main(user_groups: list):
  for user_group in user_groups:
    print('-----', user_group)
    user_group_name, description = user_group
    try:
      if not user_group_exist(user_group_name):
        create_user_group(user_group_name, description)
      else:
        raise Exception(f'A user group called "{user_group_name}" already exist')
    except Exception as e:
      print('ERROR: ', e.args)
      continue