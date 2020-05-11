# coding: utf-8
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import has_request_context, request


class RequestFormatter(logging.Formatter):

    def format(self, record):

        if has_request_context():
            record.path = request.path
            record.request_id = getattr(request, 'request_id')
        else:
            record.request_id = None
            record.path = None

        return super().format(record)


def configure_logging(app):
    formatter = RequestFormatter(
        '[%(asctime)s] [%(levelname)s] [%(path)s] '
        '[%(request_id)s] [%(message)s]'
    )
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'
    debug = app.config['DEBUG']

    if debug:
        LOG_PATH = app.config.get('LOG_PATH')
        handlers = [
            ['debug.log', logging.DEBUG],
            ['info.log', logging.INFO],
            ['error.log', logging.ERROR],
        ]

        for file_name, level in handlers:

            handler = TimedRotatingFileHandler(
                filename=os.path.join(LOG_PATH, file_name),
                encoding='utf-8',
                when='D')
            handler.setLevel(level)
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
        app.logger.debug('Logger configured in DEBUG')
    else:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        if gunicorn_logger:
            app.logger.handlers = gunicorn_logger.handlers
            for handler in app.logger.handlers:
                handler.setFormatter(formatter)
            app.logger.setLevel(gunicorn_logger.level)

            app.logger.info('Logging configured')
