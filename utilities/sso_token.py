import subprocess

from settings.logger_config import logging
from settings.credentials import (
    TALEND_SCRAPPER_USER,
    TALEND_SCRAPPER_DOMAIN,
    TALEND_SCRAPPER_PATH_COMMAND,
    TALEND_SCRAPPER_CONF_INI
)


logger = logging.getLogger(__name__)


def get_unique_sso_password() -> str:
    """this function is used only for request to SSO login and generate a unique
    sso password. this password is one time. Its necessary used the command defined
    in TALEND_SCRAPPER_PATH_COMMAND environment variable for create the password.
    """
    command = (
        f'{TALEND_SCRAPPER_PATH_COMMAND} '
        f'-conf {TALEND_SCRAPPER_CONF_INI} '
        f'-res {TALEND_SCRAPPER_DOMAIN} '
        f'-acct "{TALEND_SCRAPPER_DOMAIN}\{TALEND_SCRAPPER_USER}" '
        f'-expirecache'
    )

    try:
        output = subprocess.check_output(
            command,
            shell=True,
            executable='/bin/sh',
            stderr=subprocess.STDOUT
        ).decode('utf8').strip()
        logger.info(f"[UNIQUE SSO PASSWORD] => {output}")
        logger.info(f"[UNIQUE SSO COMMAND] => {command}")
        if 'error' in output.lower() or 'exception' in output.lower():
            logger.error(f"[UNIQUE SSO COMMAND] return error command => {command}")
            raise Exception(output)
        return output
    except subprocess.CalledProcessError as cpe:
        logger.exception(f"[UNIQUE SSO COMMAND] an unexpected error occurred to execute command {command}")
        raise Exception(cpe.output)
