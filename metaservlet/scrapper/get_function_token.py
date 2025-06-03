import pandas as pd
from settings.credentials import MANIFEST_PATH


def get_function_tokens () -> dict:
  df = pd.read_csv(MANIFEST_PATH, skiprows=1)
  ldf = df.values.tolist()
  ddf = {}
  for row in ldf:
    ddf[row[0]] = row[1].strip().split('.')[0]
  return ddf
