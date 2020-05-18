import logging
import uuid
import json
import os

from logging.config import dictConfig

from platform_agent.lib.ctime import now

logger = logging.getLogger()


class PublishLogToSessionHandler(logging.Handler):
    def __init__(self, session):
        logging.Handler.__init__(self)
        self.session = session
        self.log_id = str(uuid.uuid4())

    def emit(self, record):
        if not self.session.active:
            return
        self.session.send_log(json.dumps({
            'id': self.log_id,
            'executed_at': now(),
            'type': 'LOGGER',
            'data': {'severity': record.levelname, 'message': record.getMessage()}
        }))


def configure_logger():
    logging_config = dict(
        version=1,
        formatters={
            'f': {
                'format': '%(asctime)-24s %(levelname)-8s %(message)s'
            }
        },
        handlers={
            'h': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': int(os.environ.get('DEFAULT_LOG_LEVEL', 30))
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'f',
                'filename': os.environ['DEFAULT_LOG_FILE']
            }
        },
        root={
            'handlers': ['h', 'file'],
            'level': int(os.environ.get('DEFAULT_LOG_LEVEL', 30)),
        },
    )

    dictConfig(logging_config)
