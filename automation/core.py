from collections.abc import Callable


def run_command(command: Callable, items: list):
  for item in items:
    print('######', item)
    try:
      command(item)
      print('SUCCESS!\n')
    except Exception as e:
      print('ERROR', e.args, '\n')
      continue
    