import logging
import sys, os
from app.logger.utils import StackdriverJsonFormatter, _MaxLevelFilter


debug_handler = logging.StreamHandler(sys.stdout)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(StackdriverJsonFormatter())
debug_handler.addFilter(_MaxLevelFilter(logging.DEBUG))

# A handler for low level logs that should be sent to STDOUT
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(StackdriverJsonFormatter())
info_handler.addFilter(_MaxLevelFilter(logging.WARNING))

# A handler for high level logs that should be sent to STDERR
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(StackdriverJsonFormatter())

root_logger = logging.getLogger()

# root logger default level is WARNING, so we'll override to be DEBUG
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(info_handler)
root_logger.addHandler(error_handler)

root_logger.addHandler(debug_handler)
