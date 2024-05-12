import logging
from datetime import datetime
import os

class Logger():
    @staticmethod
    def set_logger(logfile_name: str, logfolder_path: str) -> logging.Logger:
        log_number = 1
        log_name = f'{logfile_name}'
        if not os.path.exists(logfolder_path):
            os.makedirs(logfolder_path)
        while os.path.exists(f'{logfolder_path}{os.sep}{datetime.now().strftime("%d.%m.%Y")}_{log_number:03}_{log_name}.log'):
            log_number+=1
        logging.root.setLevel(logging.NOTSET)
        file_name = f'{logfolder_path}{os.sep}{datetime.now().strftime("%d.%m.%Y")}_{log_number:03}_{log_name}.log'
        file_handler = logging.FileHandler(file_name)
        console_handler = logging.StreamHandler()
        format = logging.Formatter('%(asctime)s - %(levelname)s %(module)s: %(message)s')
        file_handler.setFormatter(format)
        console_handler.setFormatter(format)
        logger = logging.getLogger()    
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger