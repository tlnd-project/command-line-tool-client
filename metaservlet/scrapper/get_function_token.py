import pandas as pd


def get_function_tokens () -> dict:
  df = pd.read_csv('/apps/TAC/install/Talend-8.0.1/tac/apache-tomcat/webapps/org.talend.administrator/WEB-INF/deploy/administrator/rpcPolicyManifest/manifest.txt', skiprows=1)
  ldf = df.values.tolist()
  ddf = {}
  for row in ldf:
    ddf[row[0]] = row[1].strip().split('.')[0]
  return ddf
