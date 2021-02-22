import logging

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler('test.log', 'a', 'utf-8') 
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s') 
handler.setFormatter(formatter) 
root_logger.addHandler(handler)

logging.debug("A log message in level debug")
logging.info("A log message in level info")
logging.warning("A log message in level warning")
logging.error("A log message in level error")
logging.critical("A log message in level critical")