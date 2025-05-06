from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.constants import *
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
from us_visa.entity.config_entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig
from us_visa.entity.ModealFactory import ModelFactory
from us_visa.utils.main_utils import *
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from pandas import DataFrame
import numpy as np
from sklearn.pipeline import Pipeline



class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        self.model_config= read_yaml_file(MODEL_TRAINER_MODEL_CONFIG_PATH)

    def get_model_object_reports(self,train:np.array,test:np.array):
        try:
            x_train,y_train,x_test,y_test = train[:,:-1], train[:,-1],test[:,:-1],test[:,-1]
            logging.info("Train and test array is prepared")
            model_factory = ModelFactory(model_config_path=self.model_config)
            best_model_details = model_factory.best_score()

                                                                                


        except Exception as e:
            raise USVISAEXCEPTION(sys,e)


    
