import sys
from us_visa.exception import USVISAEXCEPTION
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTransformation
from us_visa.components.model_trainer import ModelTrainer
from us_visa.components.model_evaluation import ModelEvaluation
from us_visa.entity.config_entity import DataIngestionConfig ,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig
from us_visa.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,
                                            DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
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
            raise USVISAEXCEPTION(e,sys) from e
        
    def start_data_transformation(self):
        try:
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,
                                                     data_ingestion_artifact=self.start_data_ingestion(),
                                                     data_validation_artifact=self.start_data_validation())
            
            data_transformation_artifact = data_transformation.initiate_data_transformer()
            return data_transformation_artifact

        
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
    def start_model_trainer(self):
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=self.start_data_transformation(),
                                        model_trainer_config=self.model_config)
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def start_model_evaluation(self):
        try:
            model_evaluation = ModelEvaluation(data_transformation_artifact=self.start_data_transformation(),
                                               
                                               model_trainer_artifact=self.start_model_trainer(),
                                               model_evaluation_config=self.model_evaluation_config)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)

    def run_pipeline(self):
        try:
            #data_validation_artifact = self.start_data_validation()
            start_model_trainer= self.start_model_trainer()
            start_model_evaluation = self.start_model_evaluation()
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e