'''
The main server module.  
The Flask instance is exported here:
from server import server
'''

import json
import os
import logging
from flask import Flask
from typing import Dict

# Creates a new instance of Flask
app = Flask(__name__)

# import routes defined in other modules
import server.routes.alarms.route

CONFIG_PATH = "config.json"
LOG_PATH = "server.log"

def __setup_server():
    """
    Runs server setup tasks:
    - initializes the python logger for error logging
    - loads api keys into environment variables
    """
    __init_logger()
    __load_envs()


def __init_logger():
    """
    Initializes the python logger.
    """
    logging.basicConfig(
        filename=LOG_PATH,
        encoding="utf-8",
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

__setup_server()
