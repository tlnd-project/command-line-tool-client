from metaservlet.scrapper.settings import settings_update_field


def process_item(params: list):
  # TODO: maybe login before call settings_update_field and logout after
  field_name, field_value = params
  settings_update_field(field=field_name, value=field_value)
