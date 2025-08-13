
# Description of the file .env


```dotenv
# MetaservletCaller.sh
export TALEND_URL=http(s)://0.0.0.0:[port]/uri 
export TALEND_USER=user@domain.com
export IS_PASSWORD_ENCRYPTED=1 # 1 if the password is encrypt or 0 if not.
export TALEND_PASSWORD=password # prefer encrypt
export METASERVLET_CALLER=/path/fullpath/MetaservletCaller.sh
export MANIFEST_PATH=/path/fullpath/manifest.txt

# bitbuket
export ENVIRONMENT_FLAG=name_of_directory # DEV, PROD, ETC
export BITBUCKET_AUTH_TOKEN=token # Bearer Token
export BITBUCKET_REPO_BRANCH=name_of_the_branch
export BITBUCKET_REPO_URL=https:domain.com/lorem/lorem/{}?at=refs... # url of the repository

# portal web
export TALEND_SCRAPPER_SSO_FLAG=0 # 1 if SSO login it is necessary
export TALEND_SCRAPPER_SSO_URL=https:domain.com?key=val
export TALEND_SCRAPPER_SSO_USER=user
export TALEND_SCRAPPER_SSO_CONF_INI=/path/fullpath/config.ini
export TALEND_SCRAPPER_SSO_DOMAIN=DOM # the domain for the command TALEND_SCRAPPER_SSO_PATH_COMMAND
export TALEND_SCRAPPER_SSO_PATH_COMMAND=/path/fullpath/command
```