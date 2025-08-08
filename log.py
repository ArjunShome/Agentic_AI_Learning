import logging
import structlog as sl
import coloredlogs


# ANSI color codes for terminal outputs
COLOR_DEBUG = '\e[0;36m'     # cyan
COLOR_ERROR = '\e[41m'       # Red Background
COLOR_INFO = '\e[1;32m'      # Green
COLOR_CRITICAL = '\e[1;31m'  # Red 

# Custome Formatter Class
class CustomFormatter(logging.Formatter):
    formats ={
        logging.DEBUG:    COLOR_DEBUG    + '[DEBUG]    %(asctime)s - %(name)s - %(message)s',
        logging.INFO:     COLOR_INFO     + '[INFO]     %(asctime)s - %(name)s - %(message)s',
        logging.ERROR:    COLOR_ERROR    + '[ERROR]    %(asctime)s - %(name)s - %(message)s',
        logging.CRITICAL: COLOR_CRITICAL + '[CRITICAL]    %(asctime)s - %(name)s - %(message)s'
    }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno, self._fmt)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def getLogger(name):
    return sl.get_logger(name)

logger = logging.getLogger('Agentic_AI_Learning')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter())

logger.addHandler(console_handler)

# Color the logs
coloredlogs.install(level='DEBUG', logger=logger)
