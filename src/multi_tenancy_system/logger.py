import logging
import logging.config
import logging.handlers
from pathlib import Path

import yaml


def setup_logging():
    logging_config_file = Path("src/multi_tenancy_system/logging-config.yml")
    with open(logging_config_file, "r") as f:
        logging_config = yaml.safe_load(f)

    logging.config.dictConfig(logging_config)


def get_logger():
    return logging.getLogger("multi_tenancy_system")
