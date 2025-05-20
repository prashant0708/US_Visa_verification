from us_visa.exception import USVISAEXCEPTION
from us_visa.entity.estimator import USVisaModel
import sys
from pandas import DataFrame
from us_visa.configuration.aws_config import S3Client
from us_visa.logger import logging
import pickle
import io
from us_visa.entity.config_entity import S3Bucket


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
            print(f"path and bucket is passing here is {self.Bucket,model_path}")
            UsVisa_Model_s3 = USVisaEstimator.s3_key_available(self.Bucket,model_path)
            print(f"checking from is_model_present {UsVisa_Model_s3}")
            logging.info(f"Model is Available in S3 Production Bucket is {UsVisa_Model_s3}")
            return UsVisa_Model_s3
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
            
            
    def load_model(self):
        try:
            bucket= self.Bucket
            path = self.model_path
            response = self.s3.s3_client.get_object(Bucket=bucket,Key=path)
            model_binary = response['Body'].read()
            model = pickle.load(io.BytesIO(model_binary))
            return model
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
            

    def save_model(self,Body):
        try:
            if self.is_model_present(model_path=self.model_path):

                self.s3.s3_client.put_object(Bucket=self.Bucket,Key=self.model_path,Body=Body)
            else:
                print(self.Bucket)
                
                create_bucket= self.Bucket_client.create_bucket()
                logging.info(f"Model Pusher Bucket created{create_bucket}")
                self.s3.s3_client.put_object(Bucket=self.Bucket,Key=self.model_path,Body=Body)



        except Exception as e:
            raise USVisaEstimator(sys,e)


          

        
    




    
        

    


