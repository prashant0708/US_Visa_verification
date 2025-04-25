from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys

from us_visa.pipeline.training_pipeline import TrainPipeline


OBJ = TrainPipeline()

OBJ.run_pipeline()