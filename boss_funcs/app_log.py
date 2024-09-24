import logging
def get_log_level(log_level_str):
    log_level_dict = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
        'NOTSET': logging.NOTSET
    }
    return log_level_dict.get(log_level_str,logging.NOTSET)
class BossLog:
    def __init__(self,log_name=None,log_level='INFO',log_file=None) :
        if log_name:
            self.logger = logging.getLogger(log_name)
        else:
            self.logger = logging.getLogger(__name__)
        
        if not self.logger.handlers: #Avoid adding multiple handlers if the logger is already configured.
            self.logger.setLevel(get_log_level(log_level))
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            if log_file :
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)