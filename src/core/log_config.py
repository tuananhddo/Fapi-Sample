import os
import yaml
import logging.config

BASE_DIR = os.path.dirname(__file__)

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config(os.path.join(BASE_DIR, 'logging.yaml'))
logging.config.dictConfig(config)