from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys

logging.info("This is the logging test")

try:
    2/0
except Exception as e:
    logging.info(f"{USVISAEXCEPTION(e,sys) }")