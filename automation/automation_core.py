import sys
from collections.abc import Callable
from settings.credentials import CURRENT_HOST_NAME
from settings.logger_config import logging


logger = logging.getLogger(__name__)


def run_command(command: Callable, items: list):
  list_errors = []
  for item in items:
    *item_content, item_host_restriction = item

    if not item_host_restriction == "":
      item_host_restriction = item_host_restriction.split(';')
      if not CURRENT_HOST_NAME in item_host_restriction:
        continue

    try:
      logger.info(f'[RUN COMMAND] {command.__name__} ({item})')
      command(item_content)
      logger.info(f'[RUN COMMAND] {command.__name__} executed Successfully\n\n')
    except Exception as e:
      list_errors.append(type(e).__name__)
      logger.exception(f"[RUN COMMAND] {command.__name__} an unexpected error occurred: {item}")
      continue

  if len(list_errors) > 0:
    sys.exit(1)
