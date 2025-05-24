from metaservlet.api import update_user, get_user_info

def process_item(task: list):
  user_name, user_roles = task
  user_unique_id = get_user_info(user_name).get('uniqueId')
  if not user_unique_id:
    raise Exception(f'User "{user_name}" does not exist')
  update_user(user_unique_id, user_name, user_roles.split(','))
