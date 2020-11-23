"""
Helper functions for logging
"""

import logging


def log_api_call(endpoint: str, method: str, params: any):
    """
    Logs an API call from frontend.

    :params endpoint: the endpoint the api call is calling
    :params method: the HTTP method of the api call
    :params args: parameters of the api call
    """
    logging.info(
        "Server: API call from %s, method: %s params: %s",
        endpoint,
        method,
        params,
    )
