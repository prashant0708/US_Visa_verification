import sys
from us_visa.exception import USVISAEXCEPTION
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.entity.config_entity import DataIngestionConfig ,DataValidationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation(data_ingestion_artifact=DataValidationArtifact,
                                              data_validation_config=DataValidationConfig)

    def start_data_ingestion(self):
        try:
            logging.info(f"Starting the data ingestion")
            self.data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e
        
    def start_data_validation(self):
        self.data_validation.initiate_data_validation()
        
        
        self

        

    def run_pipeline(self):
        try:
            data_ingestion_artifact= self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation()
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e