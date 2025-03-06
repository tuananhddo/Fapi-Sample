import os
import yaml
import logging.config

BASE_DIR = os.path.dirname(__file__)


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def configure_logging():
    config = load_config(os.path.join(BASE_DIR, 'logging.yaml'))
    logging.config.dictConfig(config)

    # dictConfig(LogConfig(LOG_LEVEL=log_level).dict())

    gunicorn_logger = logging.getLogger("__main__")
    uvicorn_logger = logging.getLogger("uvicorn.access")
    gunicorn_logger.handlers = uvicorn_logger.handlers
    gunicorn_logger.setLevel(uvicorn_logger.level)