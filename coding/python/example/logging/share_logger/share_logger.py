import time
import logging

LOGGER_NAME = "logger.log"
FORMATTER = logging.Formatter('[%(asctime)s] %(module)s->%(funcName)s '
                              'line:%(lineno)d [%(levelname)s] %(message)s')

def get_logger(logger=None):
    logger = logging.getLogger(logger)
    logger.setLevel(logging.DEBUG)
    fh = filehandler()
    ch = streamhandler()
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def filehandler():
    fh = logging.FileHandler(LOGGER_NAME, 'a')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(FORMATTER)
    return fh

def streamhandler():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(FORMATTER)
    return ch