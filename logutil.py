import sys
import logging
import logging.handlers
import os

LOGGER_NAME = "Log"
LOG_DIR = '.log'

def setup_logging(logger_name = LOGGER_NAME, logger_file_name = '%s_log.log'%(LOGGER_NAME), logger_directory = LOG_DIR):
    max_log_file_size = 500 * 1024  # 500 KB
    max_backup_count = 10
    
    if not os.path.isdir(logger_directory):
        os.makedirs(logger_directory)
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ')
    
    # Log to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # Log to file    
    log_path = os.path.join(logger_directory, logger_file_name)
    rotating_handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=max_log_file_size, backupCount=max_backup_count)
    rotating_handler.setLevel(logging.DEBUG)
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)
    
setup_logging()
