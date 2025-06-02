from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.constants import *
import os
import boto3
from dotenv import load_dotenv

load_dotenv()
print(AWS_ACCESS_KEY_ID_ENV_KEY)
print(AWS_SECRATE_ACCESS_KEY_ENV_KEY)
class S3Client:
    s3_client =None
    s3_resource = None
    def __init__(self):
        
        """   
        This class get the aws crediential from the env and create s3 client 
        and raise exception in case of enviroment variable is not set
        """
        if S3Client.s3_client == None or S3Client.s3_resource == None:
            __access_key_id  = os.getenv("Access_key")
            __secerate_key_id = os.getenv("Secret_access_key")
            __region = REGION

            if __access_key_id is None:
                raise Exception (f"Enviroment key is not set {AWS_ACCESS_KEY_ID_ENV_KEY}")
            if __secerate_key_id is None:
                raise Exception (f"Enviroment secerate key is not set {AWS_SECRATE_ACCESS_KEY_ENV_KEY}")
            
            if __region is None:
                raise Exception(f"Region is not set {REGION}")
            
            
            
            S3Client.s3_client = boto3.client('s3',
                                              aws_access_key_id=__access_key_id,
                                                 aws_secret_access_key=__secerate_key_id,
                                                region_name= __region)
            
            S3Client.s3_resource = boto3.resource('s3',
                                              aws_access_key_id=__access_key_id,
                                                 aws_secret_access_key=__secerate_key_id,
                                                   region_name= __region)
            
            self.s3_client   =    S3Client.s3_client
            self.s3_resource =    S3Client.s3_resource

        