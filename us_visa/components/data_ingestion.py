from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.constants import *
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.configuration.mongodb_config import DB_CONNECTION
from us_visa.utils.main_utils import *
import pandas as pd
from pandas import DataFrame
import sys
from sklearn.model_selection import train_test_split


class DataIngestion:
    """
    This class will read the data from mongodb and save data 
    in Artifact folder.
    """
    def __init__ ( self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        self.MongoDB = DB_CONNECTION(DATABASE_NAME,COLLECTION_NAME)
        self.data_ingestion_config = data_ingestion_config
    
    def load_data_into_raw_folder(self) -> DataFrame:
        try:
            logging.info(f"Export the data from the Mongodb")
            collection = self.MongoDB.load_data()
            df = pd.DataFrame(list(collection.find()))
            df = drop_columns(df,cols=['_id'])
            logging.info(f"Data loaded in the DataFrame")
            os.makedirs(self.data_ingestion_config.raw_file_dir_path,exist_ok=True)
            logging.info(f"RawDir folder created {self.data_ingestion_config.raw_file_dir_path}")
            
            df.to_csv(self.data_ingestion_config.raw_data_file_path,index=False)

            logging.info(f"Data frame saved in raw folder at {self.data_ingestion_config.raw_data_file_path} ")
            
            return df
        except Exception as e:
            logging.info(f"{USVISAEXCEPTION(e,sys) }")
    
    def split_the_data(self,dataframe):
        try:
            logging.info(f"Spliting the loaded data in train and test")
            train_set , test_set = train_test_split(dataframe,test_size=TEST_SIZE)

            os.makedirs(self.data_ingestion_config.splited_file_dir_path,exist_ok=True)

            logging.info(f"Splited folder created at location  {self.data_ingestion_config.splited_file_dir_path}")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False)
            logging.info(f"""Training anf testing data save at location  
                         {self.data_ingestion_config.training_file_path,
                        self.data_ingestion_config.testing_file_path }""")
        except Exception as e:
            logging.info(f"{USVISAEXCEPTION(e,sys) }")

    def initiate_data_ingestion(self) :
        try:
            DataFrame = self.load_data_into_raw_folder()
            logging.info("Got the data from the data base")

            self.split_the_data(DataFrame)
            logging.info("Performed train test split on the dataset")
        except Exception as e:
            logging.info(f"{USVISAEXCEPTION(e,sys) }")








