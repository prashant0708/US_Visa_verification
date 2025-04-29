import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.constants import *
from us_visa.utils.main_utils import *
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact)



class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                       data_ingestion_artifact:DataIngestionArtifact,
                       data_validation_artifact:DataValidationArtifact):
        

        try:
            logging.info("Data Transformation Started")
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)