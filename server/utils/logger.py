"""
Helper functions for logging
"""

import logging

from flask import Flask
from werkzeug.wrappers import Request


# Flask middlewares require no public method.
# pylint: disable=too-few-public-methods
class LoggerMiddleware:
    """
    A middleware that logs api calls to this server
    to server.log (at the path specified in config.json)
    """

    def __init__(self, app: Flask):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ, shallow=True)

        logging.info(
            "Server: API call to %s. method: %s, params: %s",
            request.path,
            request.method,
            request.args,
        )

        return self.app(environ, start_response)


def log_exception(method: str, exception: Exception):
    """
    Logs the given exception to the log.

    :params method: The method name where the exception is raised.
    :params exception: The exception to be logged.
    """
    logging.error(
        "Exception raised from %s: %s",
        method,
        exception,
    )
