import json
import os
import sys
from evidently import Report
from evidently.presets import DataDriftPreset
from pandas import DataFrame
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.utils.main_utils import read_yaml_file,write_yaml_file,read_data
from us_visa.entity.config_entity import DataIngestionConfig,DataValidationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

SCHEMA_FILE_PATH = os.path.join('config','schema.yaml')


class DataValidation:
    def __init__(self,data_ingestion_artifact,data_validation_config):
        """ 
        param : data_ingestion_artifact : Output reference of the Data ingestion stage
        param : data_validation_config : Configuration of data validation
        param : schema_file_path : Data schema file path
        """
        try:
            logging.info("Data Validation Started")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_file_path = SCHEMA_FILE_PATH
            self.schema_config = read_yaml_file(file_path=self.schema_file_path)
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
    def validate_number_of_columns(self,df:DataFrame)->bool:
        """ 
        Method Name : validate the number of columns
        Description : This method will validate the number of columns in train and test set data
        Output : Return the boolen value based on the validation
        On Failure : Write the exception log and raise the exception
        """
        try:
            status =None
            if len(df.columns) == len(self.schema_config["columns"]):
                status = True
                logging.info(f"No of columns validated and status is    {status}")
            else :
                status= False
                logging.info(f"No of columns validated and status is    {status}")
            return status
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
    def is_columns_exists(self,df:DataFrame)->bool:
        """ 
        Method Name : is_columns_exists
        Description : This method will check all the columns specified in the schema is 
                    exists in data 
                      
        Output : Return the boolen value based on the validation
        On Failure : Write the exception log and raise the exception
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns= []
            missing_categorical_columns = []
            ## checking the numerical columns
            for column in self.schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns)>0:
                logging.info(f"missing numerical columns in data is {missing_numerical_columns}")
            else:
                logging.info(f"There is no Numerical columns missing in the data")
            ### categorical columns check
            for column in self.schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns)>0:
                logging.info(f"missing numerical columns in data is {missing_categorical_columns}")
            else:
                logging.info(f"There is no Numerical columns missing in the data")

            return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns)>0 else True   
        except  Exception as e:
            raise USVISAEXCEPTION(sys,e)
    
    def detect_data_drift(self,df_1:DataFrame,df_2:DataFrame)->bool:
        """ 
        Method Name : detect data drift
        description : Detect the data drift by comparing the train and test data 
        Output : Return the Boolen value based on the drift check
        On Failure : Write a log file and raise exception
        """
        try:
            logging.info("Data Drift checking started")
            data_drift_profile = Report([DataDriftPreset()])
            data_drift_report =data_drift_profile.run(df_1,df_2)

            report = data_drift_report.json()
            json_report = json.loads(report)
            metrics = json_report["metrics"]
            if self.data_validation_config.data_validation_drift_report_dir_name:
     
                write_yaml_file(self.data_validation_config.data_validation_drift_report_file_path,content=json_report)
            else:
                logging.info(f"Path not exists: [{self.data_validation_config.data_validation_drift_report_dir_name}]")
            #n_features = json_report["metrics"][0]["result"]["n_features"]
            feature=[]
            for i in metrics:
                col =i["metric_id"].split("column=")[-1].split(")")[0]
                feature.append(col)
            n_features=len(feature[1:])

            #n_drifted_feature = json_report["metrics"][0]["result"]["n_drifted_features"]
            n_drifted_feature=metrics[0]['value']['count']
            logging.info(f"{n_drifted_feature}/{n_features} drift detected")

            #drift_status = json_report["metrics"][0]["result"]["dataset_drift"]
            drift_status=metrics[0]['value']['share']
            return drift_status
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
    def initiate_data_validation(self)-> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            validation_message =""
            train_df = read_data(self.data_ingestion_artifact.Train_file_path)
            test_df  =read_data(self.data_ingestion_artifact.Test_file_path)
                                         
            
            ## Training data check the number of columns
            status = self.validate_number_of_columns(df=train_df)
            logging.info(f"all the required columns are present in trining data: {status}")
            if not status:
                validation_message+="Columns are missing in the Training columns"
                logging.info(f"all the required columns are not present in trining data: {status}")

            
            ## Testing data check the number of columns

            status = self.validate_number_of_columns(df=test_df)
            logging.info(f"all the required columns are present in trining data: {status}")
            if not status:
                validation_message+="Columns are missing in the Testing columns"
                logging.info(f"all the required columns are not present in trining data: {status}")

            status = self.is_columns_exists(df=train_df)
            logging.info(f"All the numerical and categorical columns are exists in training dataframe{status} ")
            if not status:
                validation_message+="Some of the training or testing Columns are missing in the training columns"
                logging.info(f"All the numerical and categorical columns are  not exists in training dataframe{status} ")

            status = self.is_columns_exists(df=test_df)
            logging.info(f"All the numerical and categorical columns are exists in testing dataframe{status} ")
            if not status:
                validation_message+="Some of the training or testing Columns are missing in the testing columns"
                logging.info(f"All the numerical and categorical columns are  not exists in testing dataframe{status} ")

            validation_status = len(validation_message) ==0

            if validation_status:
                drift_check = self.detect_data_drift(df_1=train_df,df_2=test_df)

                if drift_check:
                    logging.info(f"Data Drift detected")
                    validation_message+= "Drift Detected"
                else:
                    logging.info(f"Data Drift not detected")
                    validation_message+= "Drift not Detected"
            else:
                logging.info(f"Error in validaion: {validation_message}")
            
            data_validation_artifact = DataValidationArtifact(
                validation_status= validation_status,
                message = validation_message,
                drift_report_file_path=self.data_validation_config.data_validation_drift_report_file_path
            )

            logging.info(f"Data Validation Artifact [{data_validation_artifact}]")
            logging.info("Data Validation Pipeline Completed")

            return data_validation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        

         



