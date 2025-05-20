import sys
from us_visa.exception import USVISAEXCEPTION
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTransformation
from us_visa.components.model_trainer import ModelTrainer
from us_visa.components.model_evaluation import ModelEvaluation
from us_visa.components.model_pusher import ModelPusher
from us_visa.entity.config_entity import (DataIngestionConfig ,DataValidationConfig,DataTransformationConfig,
                                            ModelTrainerConfig,ModelEvaluationConfig,
                                            ModelPusherConfig)
from us_visa.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,
                                            DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,
                                            ModelPusherArtifact)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

        # Caching artifacts
        self.data_ingestion_artifact = None
        self.data_validation_artifact = None
        self.data_transformation_artifact = None
        self.model_trainer_artifact = None
        self.model_evaluation_artifact = None
        self.model_pusher_artifact = None

    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            self.data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return self.data_ingestion_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e

    def start_data_validation(self):
        try:
            if not self.data_ingestion_artifact:
                self.start_data_ingestion()

            data_validation = DataValidation(
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            self.data_validation_artifact = data_validation.initiate_data_validation()
            return self.data_validation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e

    def start_data_transformation(self):
        try:
            if not self.data_ingestion_artifact:
                self.start_data_ingestion()
            if not self.data_validation_artifact:
                self.start_data_validation()

            data_transformation = DataTransformation(
                data_transformation_config=self.data_transformation_config,
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_validation_artifact=self.data_validation_artifact
            )
            self.data_transformation_artifact = data_transformation.initiate_data_transformer()
            return self.data_transformation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e

    def start_model_trainer(self):
        try:
            if not self.data_transformation_artifact:
                self.start_data_transformation()

            model_trainer = ModelTrainer(
                data_transformation_artifact=self.data_transformation_artifact,
                model_trainer_config=self.model_config
            )
            self.model_trainer_artifact = model_trainer.initiate_model_trainer()
            return self.model_trainer_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e

    def start_model_evaluation(self):
        try:
            if not self.model_trainer_artifact:
                self.start_model_trainer()
            if not self.data_transformation_artifact:
                self.start_data_transformation()

            model_evaluation = ModelEvaluation(
                data_transformation_artifact=self.data_transformation_artifact,
                model_trainer_artifact=self.model_trainer_artifact,
                model_evaluation_config=self.model_evaluation_config
            )
            self.model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return self.model_evaluation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e
    
    def start_model_pusher(self):
        try:
            if not self.model_evaluation_artifact:
                self.start_model_evaluation()
            
            model_pusher = ModelPusher(model_evaluation_artifact=self.model_evaluation_artifact,
                                    model_pusher_config=self.model_pusher_config)
            
            self.model_pusher_artifact = model_pusher.initiate_model_pusher()
            return self.model_pusher_artifact
        except Exception as e:
            raise USVISAEXCEPTION(e,sys) from e

    def run_pipeline(self):
        try:
            self.start_data_ingestion()
            self.start_data_validation()
            self.start_data_transformation()
            self.start_model_trainer()
            self.start_model_evaluation()
            self.start_model_pusher()
        except Exception as e:
            raise USVISAEXCEPTION(e, sys) from e
