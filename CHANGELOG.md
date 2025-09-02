# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v3.0.0]

### Added
- It is necessary to have three repositories. Code, Keys anda Source Data. The script `refactor_deployment.sh` is responsibility doing the deployment project.
The script use the `Code` repository and set the minimal variables environment for the first execute, the file called is `.env_keys`. 
- The repository `Keys` use the two files, the `__all__` and the `.<hostname>`. The first file has the general variables for all servers and the second has
variables specific to that server. When execute the command `run-tac-command.sh <command> <source data>` the program always downloads the file `__all__` and `.<hostname>`
and merges them to building the file `.cache/.env`. The variables in `.<hostname>` has major priority and override the variable in `__all__`. If the value of whatever variable beginning with the character `#`
then it is decrypted. The format the password encrypted is `#<key_value>` therefore exists a file called `keys/<key_value>` that contained the encrypted value.
The program takes the `key_value` without the character `#` and the container of file called `keys/.<key_value>` to do the decryption.
In case it can not download the files `__all__` and  `.<hostname>` then it use the last `.cache/.env`.
It is important to mention that the password in the file `.cache/.env` is not encrypted.
- The `Source Data` repository is only for the files `<data>.txt`. If is not possible download the file or not exists then, the command fail
- Add self-test, execute validation.sh script.

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
- The run-tac-command.sh script returns the integer value when execution completes.
- If the current command did not complete successfully, the overall execution exits with the flag equal to 1.
- WORKING_DIRECTORY and CURRENT_HOST_NAME environment variables are not required, their values are taken from OS environment.

### Minor code changes
- The `params` variable in the `call_metaservlet` function was set to an empty dictionary by default.
- Command create_authorization variables were renamed using friendly code approach
- The class LocalServerClusterManagment relocation in tools/local_server_cluster_managment.py
- PEP8 format applied in the command `create_server_cluster`
- The variable `license` was renamed in command `set_license_key` and the PEP8 format was also applied
