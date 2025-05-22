from us_visa.exception import USVISAEXCEPTION
from us_visa.entity.estimator import USVisaModel
import sys
from pandas import DataFrame
from us_visa.configuration.aws_config import S3Client
from us_visa.logger import logging
from us_visa.utils.main_utils import *
from us_visa.entity.config_entity import S3Bucket
from us_visa.entity.estimator import USVisaModel


class USVisaEstimator:
    """  
    This class is used to save ,retrive us_visa model in s3 bucket and to pridict 
    """
    def __init__(self,Bucket,model_path):

        """  
        param bucket_name : Bucket name of s3 storage
        param model_path : Path of the model. 
        
        """
        self.Bucket=Bucket
        self.model_path = model_path
        self.s3= S3Client()
        self.Bucket_client = S3Bucket(Bucket_name=Bucket)
        self.loaded_model:USVisaModel=None
        

    @staticmethod    
    def get_bucket(bucket):
        S3=S3Client()
        try:
         if S3.s3_client.head_bucket(Bucket=bucket):
             return S3.s3_resource.Bucket(bucket)
         else:
             return False
        except Exception as e:
            return False
        
        
    
    @staticmethod
    def s3_key_available(bucket,path)->bool:
        
        S3=S3Client()
        buckets = USVisaEstimator.get_bucket(bucket)
        print(f"from the s3_key_available {bucket,path,bucket}")
        if not buckets:
            return False
        try:
            file_obj = [files for files in buckets.objects.filter(Prefix=path)]

            if len(file_obj)>0:
                return True
            else:
                return False
        except Exception as e:
            return False
        
    

    
        
    
    def is_model_present(self,model_path):
        """  This will check path is available of not if available return True or False"""
        try:
            
            UsVisa_Model_s3 = USVisaEstimator.s3_key_available(self.Bucket,model_path)
            
            logging.info(f"Model is Available in S3 Production Bucket is from is model present {UsVisa_Model_s3}")
            return UsVisa_Model_s3
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
            
            
    def load_model(self):
        try:
            bucket= self.Bucket
            path = self.model_path
            response = self.s3.s3_client.get_object(Bucket=bucket,Key=path)
            model_binary = response['Body'].read()
            model = dill.load(io.BytesIO(model_binary))
            return model
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
            

    def save_model(self,source_bucket,source_key):
        """
        Copies a model file from one S3 location to another.

        :param source_bucket: Source S3 bucket name
        :param source_key: Source S3 key (path to model)
    """
        try:
            copy_source={
                    'Bucket':source_bucket,
                    'Key':source_key
                }
            if self.is_model_present(model_path=self.model_path):

                #self.s3.s3_client.put_object(Bucket=self.Bucket,Key=self.model_path,Body=Body)
                self.s3.s3_client.copy_object(
                    CopySource=copy_source,
                    Bucket = self.Bucket,
                    Key = self.model_path
                )
            else:
                
                
                create_bucket= self.Bucket_client.create_bucket()
                logging.info(f"Model Pusher Bucket created{create_bucket}")
                
                self.s3.s3_client.copy_object(
                    CopySource=copy_source,
                    Bucket = self.Bucket,
                    Key = self.model_path
                )

        except Exception as e:
            raise USVisaEstimator(sys,e)
        
    def predict(self,dataframe:DataFrame):
        """
        :param dataframe:
        :return:
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe)
        except Exception as e:
            raise USVisaEstimator(sys,e)


          

        
    




    
        

    


