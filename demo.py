from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys
import posixpath
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.entity.config_entity import DataIngestionConfig ,ModelMonitortingConfig
from us_visa.configuration.aws_config import S3Client
from us_visa.pipeline.prediction_pipeline import USVisaData,usvisaclassifier
from us_visa.constants import *
import dill
from us_visa.components.data_ingestion import DataIngestion

import io

from us_visa.entity.s3_estimator import USVisaEstimator

from us_visa.configuration.aws_config import S3Client

from us_visa.maintance import ModelMonitoring

S3_Client=S3Client()


# obj = TrainPipeline()
# obj.run_pipeline()


data_ingestion= DataIngestion(data_ingestion_config=DataIngestionConfig())
obj= ModelMonitoring(data_ingestion_artifact=data_ingestion.initiate_data_ingestion(),model_monitoring_config=ModelMonitortingConfig())

obj.initiate_model_monitoring()

