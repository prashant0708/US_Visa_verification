from us_visa.Data_insersion_mangodb.mongo import Mongo_connection,load_data


connection = Mongo_connection("US_VISA","Visa_Data")

load_data = load_data(connection)