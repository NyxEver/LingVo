import os
import logging
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(os.path.dirname(current_dir))
logs_dir = os.path.join(main_dir, "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

def get_logger(name):
    """日志模块"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        logger.handlers.clear()

    today_time = datetime.now().strftime("%Y-%m-%d")

    log_file=os.path.join(logs_dir, f"log_{today_time}.txt")
    file_handler = logging.FileHandler(log_file,encoding="utf-8")
    console_handler = logging.StreamHandler()

    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    log_formatter=logging.Formatter('|%(asctime)s| - |%(levelname)s| - |%(filename)s:%(lineno)d| - %(message)s')
    file_handler.setFormatter(log_formatter)
    console_handler.setFormatter(log_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger