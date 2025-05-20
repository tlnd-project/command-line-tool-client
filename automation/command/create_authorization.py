from automation.command.delete_authorization import (
    process_item as revoke_authorization_command,
)
from metaservlet.api import create_authorization


def process_item(authorization: list):
  _type, project_name, group_name = authorization
  revoke_authorization_command([project_name, group_name])
  create_authorization(project_name, group_name, _type)
