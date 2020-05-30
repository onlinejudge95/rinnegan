from app import create_app

import coloredlogs
import logging
import logging.config
import os
import yaml


def setup_logging():
    with open("/usr/src/app/logging.yml", "r") as fp:
        try:
            config_dict = yaml.safe_load(fp.read())
            logging.config.dictConfig(config_dict)
            coloredlogs.install()
        except Exception as e:
            print(e)
            print("There is an error in the logging configuration")
        else:
            logging.info("Logging setup finished successfully")


setup_logging()
app = create_app(os.getenv("FLASK_ENV"))
