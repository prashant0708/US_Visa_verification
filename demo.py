from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact


OBJ = TrainPipeline()

OBJ.run_pipeline()