import pandas as pd
import sys
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from sklearn.pipeline import Pipeline
from pandas import DataFrame




class TargetValueMapping:
    def __init__(self):
        self.Certified :int = 1
        self.Denied:int = 0

    def asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        reverse_mapping_value = self.asdict()
        return dict(zip(reverse_mapping_value.values(),reverse_mapping_value.keys()))
    

class USVisaModel:
    def __init__(self,preprocessing_obj:Pipeline,trained_object_model:object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_obj=preprocessing_obj
        self.trained_object_model=trained_object_model

    def predict(self,data_frame:DataFrame):
        """
        This Function will accept the raw inputs and transformed it using preprocessing_obj.
        which will transform the raw input into formate that model can accept and use for prediction

        """
        logging.info("Prediction is started")
        try:
            logging.info("Using the trained model to get the prediction")
            transformed_feature = self.preprocessing_obj.transform(data_frame)
            logging.info("Using the trained model to predict")
            prediction= self.trained_object_model.predict(transformed_feature)
            return prediction

        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
        
