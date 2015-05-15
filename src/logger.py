import logging
import sys

logger = logging.getLogger('invenio')
logger_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger_stream = logging.StreamHandler(sys.stderr)
logger_stream.setFormatter(logger_formatter)
logger.addHandler(logger_stream)
logger.setLevel(logging.DEBUG)
