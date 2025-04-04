from metaservlet.api import delete_user, user_exists


def process_item(user: list):
  if not user_exists(user[0]):
    raise Exception(f'A user called {user[0]} does not exist')

  delete_user(user[0])
