"""
The main server module.
The Flask instance is exported here:
from server import server
"""

import json
import os
import logging
from typing import Dict
from flask import Flask

from server.utils.logger import LoggerMiddleware

CONFIG_PATH = "config.json"


def __setup_server():
    """
    Runs server setup tasks:
    - loads server configuration into environment variables
    - initializes the python logger for error logging
    """
    __load_envs()
    __init_logger()


def __init_logger():
    """
    Initializes the python logger.
    """
    logging.basicConfig(
        filename=os.environ["SERVER_LOG_PATH"],
        level=logging.DEBUG,
    )

def __load_envs():
    """
    Load config constants and api keys into environment variables.
    """
    with open(CONFIG_PATH, "r") as config_file:
        # load json key val pairs into a dict
        configs: Dict[str, str] = json.load(config_file)

        for key, val in configs.items():
            os.environ[key.upper()] = val


# === server initialization === #


__setup_server()

# Creates a new instance of Flask
app = Flask(__name__, template_folder=os.environ["TEMPLATES_PATH"])

# Registers our LoggerMiddleware
# app.wsgi_app = LoggerMiddleware(app)

# Import routes defined in other modules.
# ignoring pylint warning here because this import is used to initialize Flask routes
# and they must be imported *after* Flask is initialized.
# pylint: disable=wrong-import-position, unused-import
import server.routes
