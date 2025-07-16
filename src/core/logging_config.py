import os
import logging
from datetime import datetime

if not os.path.exists("logs"):
    os.makedirs("logs")

def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        logger.handlers.clear()

    today_time = datetime.now().strftime("%Y-%m-%d")

    file_handler = logging.FileHandler(f"logs/log_{today_time}.txt",encoding="utf-8")
    console_handler = logging.StreamHandler()

    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    log_formatter=logging.Formatter('|%(asctime)s| - |%(levelname)s| - |%(filename)s:%(lineno)d| - %(message)s')
    file_handler.setFormatter(log_formatter)
    console_handler.setFormatter(log_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger