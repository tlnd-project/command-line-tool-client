import os
import shutil
import uuid
import tarfile
import csv
import requests
from settings.logger_config import logging
from settings.credentials import WORKING_DIRECTORY, BITBUCKET_AUTH_TOKEN, BITBUCKET_REPO_URL, BITBUCKET_REPO_BRANCH, ENVIRONMENT_FLAG

logger = logging.getLogger(__name__)


def create_directory(path, force_create=False):
  try:
    os.mkdir(path)
  except FileExistsError:
    if force_create:
      shutil.rmtree(path)
      os.mkdir(path)

def download_project_tar_gz(file_name):
  headers = {
    'Authorization': f'Bearer {BITBUCKET_AUTH_TOKEN}'
  }
  new_url = BITBUCKET_REPO_URL.split("raw")[0]
  response = requests.get(
    f"{new_url}archive?at=refs%2Fheads%2Frelease%2F{BITBUCKET_REPO_BRANCH}&format=tar.gz",
    verify=False,
    stream=True,
    headers=headers
  )
  response.raise_for_status()

  with open(file_name, "wb") as f:
    for chunk in response.iter_content(1024):
      f.write(chunk)

def find_txt_files(directory):
  _files = []
  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".txt"):
        _files.append(os.path.join(root, file))
  return _files

def validate_csv(files_txt, required_columns=None):
  for file_name in files_txt:
    logger.info(f"Validating the file {file_name} .... ")
    with open(file_name, 'r', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile, delimiter='|')
      rows = list(reader)

      if not rows:
        logger.error(f"File {file_name} has no rows")
        continue
      header = rows[0]
      expected_columns = len(header)

      for i, row in enumerate(rows[1:], start=2):
        if len(row) != expected_columns:
          logger.error(f"Error: unexpected columns in the line {i}  = {len(row)} != {expected_columns}")

def validate_all_txt_from_project():
  # create a temp directory
  temp_directory = os.path.join(WORKING_DIRECTORY, str(uuid.uuid4()))
  create_directory(temp_directory)

  # download the repository .tar.gz
  file_name = os.path.join(temp_directory, f"{BITBUCKET_REPO_BRANCH}.tar.gz")
  download_project_tar_gz(file_name)

  # unzip the repository
  with tarfile.open(file_name) as tar:
    tar.extractall(path=temp_directory)

  # find all files with .txt extension
  project_directory = os.path.join(temp_directory, f"DeploymentFiles/{ENVIRONMENT_FLAG}")
  files_txt = find_txt_files(project_directory)

  # verify the format CSV.
  validate_csv(files_txt)

  # remove the directory
  shutil.rmtree(temp_directory)
