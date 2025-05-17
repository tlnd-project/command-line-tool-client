import ast

from metaservlet.core import tac_client
from get_function_token import get_function_tokens
from settings.credentials import TALEND_USER, TALEND_PASSWORD

TAC_PERMUTATION = "17B18BA3641F02EA98896D1400E44444"
TAC_FIELDS = {
  "artifact_repository": {
    "password": 34
  },
  "software_update": {
    "local_deployment_password": 121,
    "local_reader_password": 123
  },
  "ldap": {
    "admin_password": 72
  },
  "smtp": {
    "from_address": 107
  }
}
function_tokens = get_function_tokens()

def settings_update_field(field, value):
  _field = field.split(".")  # p/e: ldap.admin_password => ['ldap', 'admin_password']
  try:
    _first_key = _field[0]
    _second_key = _field[1]
  except IndexError:
    raise Exception(f"The value: {field} is not has a format `section.field`")

  try:
    _val = TAC_FIELDS[_first_key][_second_key]
  except KeyError:
    raise Exception(f"The field: {field} is not found in TAC support fields")

  # 1) login
  rq_1_body = (
    '7|0|7|https://satacd0001:8443/org.talend.administrator/administrator/'
    f"|{function_tokens['org.talend.gwttoolkit.client.login.service.LoginService']}"
    '|org.talend.gwttoolkit.client.login.service.LoginService'
    f'|login|java.lang.String/2004016611|{TALEND_USER}|{TALEND_PASSWORD}|1|2|3|4|2|5|5|6|7|'
  ).encode('utf-8')
  rq_1_headers = {
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
    'Host': 'satacd0001:8443',
    'Origin': 'https://satacd0001:8443',
    'Referer': 'https://satacd0001:8443/org.talend. administrator/',
  }
  # tac_client.session.cookies.set('talendremember', 'false')
  # tac_client.session.cookies.set('lang', 'en')
  response = tac_client.post(
    endpoint="administrator/login",
    data=rq_1_body,
    headers=rq_1_headers,
    verify=False,
    allow_redirects=True
  )
  print(response.headers)
  print('')
  print(response.text)

  # tac_client.session.cookies.set('talendremember', 'false')
  # tac_client.session.cookies.set('lang', 'en')
  headers = {
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
    'Host': 'satacd0001:8443',
    'Origin': 'https://satacd0001:8443',
    'Referer': 'https://satacd0001:8443/org.talend. administrator/',
    'X-GWT-Module-Base': 'https://satacd0001:8443/org.talend.administrator/administrator/',
    'X-GWT-Permutation': TAC_PERMUTATION,
  }
  data = (
    '7|0|4|https://satacd0001:8443/org.talend.administrator/administrator/'
    f"|{function_tokens['com.google.gwt.user.client.rpc.XsrfTokenService']}"
    '|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|'
  ).encode('utf-8')

  response_2 = tac_client.post(
    endpoint='administrator/xsrf',
    data=data,
    headers=headers,
    verify=False,
    allow_redirects=True,
  )
  print(response_2.request.headers)
  print(response_2.headers)
  print(response_2.text)
  xsrf = ast.literal_eval(response_2.text.replace("//OK", "'"))

  # 2) update field

  request_3_data = (
    '17|2|9|https://satacd0001:8443/org.talend.administrator/administrator/'
    f"|{function_tokens['org.talend.gwtadministrator.client.module.settings.configuration.service.ConfigService']}"
    f"|{xsrf[2][0]}|{xsrf[2][1]}"
    '|org.talend.gwtadministrator.client.module.settings.configuration.service.ConfigService'
    '|saveConfigValue|org.talend.gwtadministrator.client.module.settings.configuration.model.enums.Config/3074497691'
    f'|java.lang.String/2004016611|{value}|1|2|3|4|5|6|2|7|8|7|{_val}|9|'
  ).encode('utf-8')

  response_3 = tac_client.post(
    'https://satacd0001:8443/org.talend.administrator/administrator/config',
    headers=headers,
    data=request_3_data,
    verify=False,
    allow_redirects=True,
  )

  print(response_3.request.headers)
  print(response_3.headers)
  print(response_3.text)

  # 3) logout

  logout_data = (
    '7|0|4|https://satacd0001:8443/org.talend.administrator/administrator/'
    f"|{function_tokens['org.talend.gwttoolkit.client.login.service.LoginService']}"
    '|org.talend.gwttoolkit.client.login.service.LoginService|logout|1|2|3|4|0|'
  )
  # tac_client.session.cookies.set('talendremember','false')
  # tac_client.session.cookies.set ('lang', 'en')

  response_4 = tac_client.post(
    endpoint='administrator/login',
    headers = rq_1_headers,
    data = logout_data,
    verify=False,
    allow_redirects=True,
  )

  print(response_4.request.headers)
  print(response_4.headers)
  print(response_4.text)
