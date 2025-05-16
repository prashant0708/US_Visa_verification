from us_visa.exception import USVISAEXCEPTION
from us_visa.entity.estimator import USVisaModel
import sys
from pandas import DataFrame
from us_visa.configuration.aws_config import S3Client
from us_visa.logger import logging
import pickle



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

    @staticmethod    
    def get_bucket(bucket):
        S3=S3Client()
        bucket = S3.s3_resource.Bucket(bucket)
        return bucket 
    
    @staticmethod
    def s3_key_available(bucket,path)->bool:
        S3=S3Client()
        bucket = USVisaEstimator.get_bucket(bucket)
        file_obj = [files for files in bucket.objects.filter(Prefix=path)]

        if len(file_obj)>0:
            return True
        else:
            return False
    
    def is_model_present(self,model_path):
        """  This will check path is available of not if available return True or False"""
        try:
            UsVisa_Model_s3 = USVisaEstimator.s3_key_available(self.bucket,model_path)
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
            model = pickle.load(model_binary)
            return model
        except Exception as e:
            raise USVisaEstimator(sys,e)
            

    def save_model(self,Body):
        try:
            self.s3.s3_client.put_object(Bucket=self.Bucket,Key=self.self.model_path,Body=Body)

        except Exception as e:
            raise USVisaEstimator(sys,e)


          

        
    




    
        

    


