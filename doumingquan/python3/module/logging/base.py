import logging

# logging.config.fileConfig("./logging.conf")
logging.basicConfig(filename='logger.log', level=logging.INFO)

# create logger
logger_name1 = "example01"
logger = logging.getLogger(logger_name1)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

