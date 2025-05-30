import os
import logging.config
import logging.handlers
from .credentials import WORKING_DIRECTORY, LOG_LEVEL, LOG_NAME


LOGS_ROOT = os.path.join(WORKING_DIRECTORY, 'logs')
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] {name} | {message}',
            'style': '{',
        },
        'detailed': {
            'format': '[{asctime}] [{levelname}] {name} | {message}\n{exc_info}',
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_ROOT, LOG_NAME),
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': LOG_LEVEL,
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
