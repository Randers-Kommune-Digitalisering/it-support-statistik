import sys
import logging

from utils.config import DEBUG


# Logging configuration
def set_logging_configuration():
    log_level = logging.DEBUG if DEBUG else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=log_level, format='[%(asctime)s] %(levelname)s - %(name)s - %(module)s:%(funcName)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
