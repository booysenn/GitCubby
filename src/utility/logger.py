import logging
import sys
from pathlib import Path

from .constants import LOG_FILE_PATH, LOG_FORMAT, DATE_FORMAT

class GCLogger:

    def __init__(self, name, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.get_logger()
        self.set_log_level(log_level)


    def get_logger(self):
        """
        Get a logger instance for a module
        
        Args:
            name: Usually __name__ from the calling module
        
        Returns:
            logging.Logger: Configured logger instance
        """
        
        # Only configure if not already configured
        if not self.logger.handlers:
        
            if not LOG_FILE_PATH.exists():
                LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
                LOG_FILE_PATH.touch()
                LOG_FILE_PATH.chmod(0o666)

            self.logger.setLevel(logging.INFO)
            
            # File handler
            file_handler = logging.FileHandler(str(LOG_FILE_PATH))
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
            file_handler.setFormatter(file_formatter)
            
            # Console handler (for errors and warnings)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        return self.logger

    def set_log_level(self,level):
        """
        Set the global log level
        
        Args:
            level: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR
        """
        self.logger.setLevel(level)