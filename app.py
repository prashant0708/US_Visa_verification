from us_visa.Data_insersion_mangodb.mongo import Mongo_connection,load_data
from us_visa.logger import logging


# connection = Mongo_connection("US_VISA","Visa_Data")

# load_data = load_data(connection)

logging.info("Logging of the file started")

result = 5/0
logging.error(result)
