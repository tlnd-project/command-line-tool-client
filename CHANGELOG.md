# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### other changes
- in command create_authorization the variables rename a code friendly
- the class LocalServerClusterManagment relocation in tools/local_server_cluster_managment.py
- in command create_server_cluster apply pep8
- in command set_license_key apply pep8, rename the variable `license`

### review
- in delete_users_from_group.py there is not changes.
- in delete_user_group.py there is not changes.
- in create_user_group.py there is not changes.
- review in create_project.py, add conditional if=='git'
- do I need to add BITBUCKET_REPO_BRANCH or did it already exist?


## [v2.0.0] - 2025-06-30

### Added
- New command `remove_server_cluster`
- Add the file soteri-security.yml
- set `MANIFEST_PATH` in .env file. It is the path of the file manifest.txt
- Implement logger inside /logs directory. set default `LOG_LEVEL` and `LOG_NAME` with "INFO" and "command.log".
- Support SSO Login wih unique password for `update_tac_settings`. Set the environment variables `TALEND_SCRAPPER_SSO_FLAG`, `TALEND_SCRAPPER_DOMAIN`, `TALEND_SCRAPPER_PATH_COMMAND`, `TALEND_SCRAPPER_CONF_INI`
- New command `update_tac_settings`. Set the environment variables `TALEND_SCRAPPER_URL`, `TALEND_SCRAPPER_USER`, `TALEND_SCRAPPER_PASSWORD`
- if the password for talend scrapper is encrypted then use the program .jar for decrypter.
- New command `update_user`

### Changed
- The script run-tac-command.sh return the value integer when finally the executing. The value is zero if executed was successfully
- If there are one command that not finally success, then general execution exist with flag equal a 1.
- The variable `params` set empty dict by default in `call_metaservlet` function
- WORKING_DIRECTORY and CURRENT_HOST_NAME environment variables is not required, now is calculated.
