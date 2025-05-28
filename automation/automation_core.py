import sys
from collections.abc import Callable
from settings.credentials import CURRENT_HOST_NAME


def run_command(command: Callable, items: list):
  list_errors = []
  for item in items:
    *item_content, item_host_restriction = item

    if not item_host_restriction == "":
      item_host_restriction = item_host_restriction.split(';')
      if not CURRENT_HOST_NAME in item_host_restriction:
        continue

    print('######')
    try:
      command(item_content)
      print('SUCCESS!\n')
    except Exception as e:
      list_errors.append(type(e).__name__)
      print('ERROR', e.args, '\n')
      continue

  if len(list_errors) > 0:
    sys.exit(1)
