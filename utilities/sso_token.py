import subprocess
import os.path

from settings.credentials import (TALEND_SCRAPPER_USER,
                                  TALEND_SCRAPPER_DOMAIN,
                                  TALEND_SCRAPPER_PATH_COMMAND,
                                  TALEND_SCRAPPER_CONF_INI)


def get_unique_sso_password() -> str:
    command = f'{TALEND_SCRAPPER_PATH_COMMAND} --conf {TALEND_SCRAPPER_CONF_INI} -res {TALEND_SCRAPPER_DOMAIN} -actt {TALEND_SCRAPPER_DOMAIN}/{TALEND_SCRAPPER_USER} -expirecache'
    try:
        output = subprocess.check_output(
            command,
            shell=True,
            executable='/bin/sh',
            stderr=subprocess.STDOUT
        ).decode('utf8').strip()
        if 'error' in output.lower() or 'exception' in output.lower():
            raise Exception(output)
        return output
    except subprocess.CalledProcessError as cpe:
        raise Exception(cpe.output)
