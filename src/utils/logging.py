import sys
import logging

from prometheus_client import Gauge

from utils.config import DEBUG

# Prometheus metricts
# Availavility metrics
is_ready_gauge = Gauge('is_ready', '1 - app is running, 0 - app is down', labelnames=['error_type', 'job_name'])
last_updated_gauge = Gauge('last_updated_ms', "Timestamp in milliseconds of the last time the app's availability was updated")

# Dependency metrics
is_available_gauge = Gauge('is_available', '1 - dependency is available, 0 - dependency is not available', labelnames=['dependency_name'])


# Logging configuration
def set_logging_configuration():
    log_level = logging.DEBUG if DEBUG else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=log_level, format='[%(asctime)s] %(levelname)s - %(name)s - %(module)s:%(funcName)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
