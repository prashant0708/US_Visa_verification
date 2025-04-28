import sys
from us_visa.exception import USVISAEXCEPTION
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.entity.config_entity import DataIngestionConfig ,DataValidationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingstion_artifact=data_ingestion.initiate_data_ingestion()
            return data_ingstion_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e
        
    def start_data_validation(self):
        try:
            data_validation = DataValidation(data_ingestion_artifact=self.start_data_ingestion(),
                                             data_validation_config=self.data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e
    def run_pipeline(self):
        try:
            data_validation_artifact = self.start_data_validation()
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e