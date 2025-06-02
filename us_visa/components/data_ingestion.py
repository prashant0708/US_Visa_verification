from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.constants import *
from us_visa.entity.config_entity import DataIngestionConfig,S3Bucket
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.configuration.mongodb_config import DB_CONNECTION
from us_visa.utils.main_utils import *
import pandas as pd
from pandas import DataFrame
import sys
from sklearn.model_selection import train_test_split
from us_visa.configuration.aws_config import S3Client
import io


class DataIngestion:
    """
    This class will read the data from mongodb and save data 
    in Artifact folder.
    """
    def __init__ ( self,data_ingestion_config:DataIngestionConfig):
        logging.info("Data Ingestion Started")
        self.MongoDB = DB_CONNECTION(DATABASE_NAME,COLLECTION_NAME)
        self.data_ingestion_config = data_ingestion_config
        self.data_ingstion_artifact = DataIngestionArtifact
        self.s3cilent = S3Client()
    
    def load_data_into_raw_folder(self) -> DataFrame:
        try:
            logging.info(f"Export the data from the Mongodb")
            collection = self.MongoDB.load_data()
            df = pd.DataFrame(list(collection.find()))
            df = drop_columns(df,cols=['_id'])
            logging.info(f"Data loaded in the DataFrame")
            #os.makedirs(self.data_ingestion_config.raw_file_dir_path,exist_ok=True)
            ## Calling bucket function to create bucket
            S3_Client = S3Bucket(Bucket_name=BUCKET_NAME)
            Create_Bucket= S3_Client.create_bucket()
            logging.info(f"S3 Bucket created{Create_Bucket}")
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer,index=False)
            logging.info("DataFrame saved in csv memory location")
            self.s3cilent.s3_client.put_object(Bucket=BUCKET_NAME,Key =self.data_ingestion_config.raw_data_file_path,
                                               Body= csv_buffer.getvalue() )
            logging.info(f"Data  saved in raw folder at [{self.data_ingestion_config.raw_data_file_path}] ")
            return df
        except Exception as e:
            logging.info(f"{USVISAEXCEPTION(e,sys) }")
    
    def split_the_data(self,dataframe):
        try:
            logging.info(f"Spliting the loaded data in train and test")
            train_set , test_set = train_test_split(dataframe,test_size=TEST_SIZE)

            #os.makedirs(self.data_ingestion_config.splited_file_dir_path,exist_ok=True)

            logging.info(f"Splited folder created at location  [{self.data_ingestion_config.splited_file_dir_path}]")
            train_csv_buffer = io.StringIO()
            test_csv_buffer = io.StringIO()

            train_set.to_csv(train_csv_buffer,index=False)

            self.s3cilent.s3_client.put_object(Bucket=BUCKET_NAME,Key =self.data_ingestion_config.training_file_path,
                                               Body= train_csv_buffer.getvalue() )
            
            test_set.to_csv(test_csv_buffer,index=False)

            self.s3cilent.s3_client.put_object(Bucket=BUCKET_NAME,Key =self.data_ingestion_config.testing_file_path,
                                               Body= test_csv_buffer.getvalue() )            
            logging.info(f"""Training and testing data save at location  
                         [{self.data_ingestion_config.training_file_path,'*****',
                        self.data_ingestion_config.testing_file_path }]""")
        except Exception as e:
            logging.info(f"{USVISAEXCEPTION(e,sys) }")

    def initiate_data_ingestion(self)->DataIngestionArtifact :
        try:
            DataFrame = self.load_data_into_raw_folder()
            

            self.split_the_data(DataFrame)
            
            data_ingestion_artifact = self.data_ingstion_artifact(Test_file_path=self.data_ingestion_config.training_file_path,Train_file_path=self.data_ingestion_config.training_file_path)
            
            logging.info("Data Ingestion Pipeline completed")

            return data_ingestion_artifact
            

            
        except Exception as e:
            logging.info(f"{USVISAEXCEPTION(e,sys) }")








