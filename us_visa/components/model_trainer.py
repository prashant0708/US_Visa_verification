from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.constants import *
import io
from us_visa.configuration.aws_config import S3Client
from us_visa.entity.artifact_entity import (DataIngestionArtifact,DataTransformationArtifact,
                                          ClassificationMetricArtifact,ModelTrainerArtifact)
from us_visa.entity.config_entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig
from us_visa.entity.ModealFactory import ModelFactory
from us_visa.utils.main_utils import *
from us_visa.entity.estimator import USVisaModel
from us_visa.constants import *
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from pandas import DataFrame
import numpy as np
from sklearn.pipeline import Pipeline




class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        self.model_config_path= MODEL_TRAINER_MODEL_CONFIG_PATH
        self.S3Client = S3Client()
        

    def get_model_object_reports(self,train:np.array,test:np.array):
        try:
            x_train,y_train,x_test,y_test = train[:,:-1], train[:,-1],test[:,:-1],test[:,-1]
            logging.info("Train and test array is prepared")
            model_factory = ModelFactory(model_config_path=self.model_config_path)
            best_model_details = model_factory.best_score(X=x_train,Y=y_train,best_score=MODEL_TRAINER_EXPECTED_ACCURACY)
            model_obj = best_model_details.best_model
            y_pred = model_obj.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred) 
            f1 = f1_score(y_test, y_pred)  
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            metric_artifact = ClassificationMetricArtifact(f1_score=f1,precision_score=precision,
                                                           recall_score=recall)
            
            logging.info(f"Details of Model [{best_model_details,metric_artifact}]")
            return best_model_details,metric_artifact
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def initiate_model_trainer(self):

        logging.info("Starting the model trainer ")
        try:
            

            #train_arr =load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            train_array_path = self.data_transformation_artifact.transformed_train_file_path
            train_arr= load_numpy_array_data_s3(s3=self.S3Client,key=train_array_path,Bucket=BUCKET_NAME)
            test_array_path = self.data_transformation_artifact.transformed_test_file_path
            test_arr = load_numpy_array_data_s3(s3=S3Client,key=test_array_path,Bucket=BUCKET_NAME)
            #preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            preprocessing_obj_path = self.data_transformation_artifact.transformed_object_file_path

            preprocessing_obj = load_object_s3(s3=S3Client,key=preprocessing_obj_path,Bucket=BUCKET_NAME)


            best_model_details,metric_artifact = self.get_model_object_reports(train=train_arr,test=test_arr)
            
            if best_model_details.best_score<MODEL_TRAINER_EXPECTED_ACCURACY:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")
            us_visa_model = USVisaModel(preprocessing_obj=preprocessing_obj,
                                        trained_object_model=best_model_details.best_model)
            logging.info("Created usvisa model object with preprocessor and model")
           
            #save_object(self.model_trainer_config.model_trainer_trained_model_path,us_visa_model)
            buffer_obj=save_object_s3(us_visa_model)
            load_data_to_s3(Bucket=BUCKET_NAME,path=self.model_trainer_config.model_trainer_trained_model_path,
                                S3Client=S3Client,Body=buffer_obj)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.model_trainer_trained_model_path,
                                                      metric_artifact=metric_artifact)
            logging.info(f"Model Trainer Artifact [{model_trainer_artifact}]")
            return model_trainer_artifact
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
    


        


                                                                                


        


    
