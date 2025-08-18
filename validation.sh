#!/bin/sh
#-------------------------------------------------------------------------------
# Shell Script: test-tac-automation
# Description: This script runs the test functions, so the tac-automation project
#              must be installed
# Author: Ricardo Bermudez Bermudez
# Usage: bash validation.sh
# Version: 0.1
#-------------------------------------------------------------------------------

source .env

directory="test_tac_automation"
if [ ! -d "$directory" ]; then
  mkdir ./"$directory"
fi

version_file="0.1"
file_name_to_array=("self_test.py" "test_bitbucket.py" "test_decrypt.py" "test_files_csv.py" "test_metaservlet.py" "test_scrapper.py")
token=$(java -jar dtcc.jar decrypt settings/dtcc_bbk.key "$BITBUCKET_AUTH_TOKEN")

for file in "${file_name_to_array[@]}"; do
  url_download_file=${BITBUCKET_REPO_URL/\{\}/$ENVIRONMENT_FLAG/${file}_${version_file}}$BITBUCKET_REPO_BRANCH
  curl -s -S -H "Authorization: Bearer $token" \
       -o "$directory/$file" \
       -L "$url_download_file"
done

# particular case __init__.py_0.8
url_download_file=${BITBUCKET_REPO_URL/\{\}/$ENVIROMENT_FLAG/__init__.py_8.0}$BITBUCKET_REPO_BRANCH
curl -s -S -H "Authorization: Bearer $token" \
       -o "$directory/__init__.py" \
       -L "$url_download_file"

source venv/bin/activate
python "$directory/self_test.py"
