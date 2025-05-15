import requests, urllib3
from requests.cookies import create_cookie
import ast
from get_function_token import get_function_tokens

urllib3.disable_warnings()

function_tokens = get_function_tokens()

session = requests.Session()
session.cookies.set('talendremember', 'false')
session.cookies.set ('lang', 'en')

rq_1_url = 'https://satacd0001:8443/org.talend.administrator/administrator/login'
rq_1_headers = {
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
  'Host': 'satacd0001:8443',
  'Origin': 'https://satacd0001:8443',
  'Referer': 'https://satacd0001:8443/org.talend. administrator/',
}

rq_1_body = (
  '7|0|7|https://satacd0001:8443/org.talend.administrator/administrator/'
  f"|{function_tokens['org.talend.gwttoolkit.client.login.service.LoginService']}"
  '|org.talend.gwttoolkit.client.login.service.LoginService'
  '|login|java.lang.String/2004016611|taladm@dtcc.com|T@lend2023|1|2|3|4|2|5|5|6|7|'
).encode('utf-8')

response = session.post(
  rq_1_url,
  headers = rq_1_headers,
  data = rq_1_body,
  verify=False,
  allow_redirects=True
)

print(response.headers)
print('')
print(response.text)


session.cookies.set('talendremember', 'false')
session.cookies.set ('lang', 'en')

headers = {
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
  'Host': 'satacd0001:8443',
  'Origin': 'https://satacd0001:8443',
  'Referer': 'https://satacd0001:8443/org.talend. administrator/',
  'X-GWT-Module-Base': 'https://satacd0001:8443/org.talend.administrator/administrator/',
  'X-GWT-Permutation': '17B18BA3641F02EA98896D1400E44444',
}

data = (
  '7|0|4|https://satacd0001:8443/org.talend.administrator/administrator/'
  f"|{function_tokens['com.google.gwt.user.client.rpc.XsrfTokenService']}"
  '|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|'
).encode('utf-8')

response_2 = session.post (
  'https://satacd0001:8443/org.talend.administrator/administrator/xsrf',
  headers = headers,
  data = data,
  verify=False,
  allow_redirects=True,
)

print('')

print(response_2.request.headers)
print(response_2.headers)
print(response_2.text)

xsrf = ast.literal_eval(response_2.text.replace("//OK", "'"))


request_3_data = (
  '17|2|9|https://satacd0001:8443/org.talend.administrator/administrator/'
  f"|{function_tokens['org.talend.gwtadministrator.client.module.settings.configuration.service.ConfigService']}"
  f"|{xsrf[2][0]}|{xsrf[2][1]}"
  '|org.talend.gwtadministrator.client.module.settings.configuration.service.ConfigService'
  '|saveConfigValue|org.talend.gwtadministrator.client.module.settings.configuration.model.enums.Config/3074497691'
  '|java.lang.String/2004016611|taladm1234@dtcc.com|1|2|3|4|5|6|2|7|8|7|107|9|'
).encode('utf-8')

response_3 = session.post (
  'https://satacd0001:8443/org.talend.administrator/administrator/config',
  headers = headers,
  data = request_3_data,
  verify = False,
  allow_redirects = True,
)

print(response_3.request.headers)
print(response_3.headers)
print(response_3.text)

logout_data = (
  '7|0|4|https://satacd0001:8443/org.talend.administrator/administrator/'
  f"|{function_tokens['org.talend.gwttoolkit.client.login.service.LoginService']}"
  '|org.talend.gwttoolkit.client.login.service.LoginService|logout|1|2|3|4|0|'
)
session.cookies.set('talendremember','false')
session.cookies.set ('lang', 'en')

response_4 = session.post(
  rq_1_url,
  headers = rq_1_headers,
  data = logout_data,
  verify=False,
  allow_redirects=True,
)

print(response_4.request.headers)
print(response_4.headers)
print(response_4.text)
