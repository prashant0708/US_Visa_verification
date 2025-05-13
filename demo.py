from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys
import posixpath

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from us_visa.configuration.aws_config import S3Client
from us_visa.constants import *


## create a bucket

s3cilent = S3Client()

Bucket_name="us-visa-mlops"



# if REGION  == CHECK_REGION:
#     s3cilent.s3_client.create_bucket(Bucket = Bucket_name)
# else:
#     localtion={'LocationConstraint':REGION}
#     s3cilent.s3_client.create_bucket(Bucket = Bucket_name,
#                                      CreateBucketConfiguration=localtion
#                                      )
    
#     print(f"Bucket create at location{REGION},{Bucket_name}")


# artifact_dir = posixpath.join(ARTIFACT_DIR_NAME,PIPELINE_NAME,CURRENT_TIME_STEMP)+"/"
# data_ingestion = posixpath.join(artifact_dir,DATA_INGESTION_DIR_NAME)+"/"
# s3_file_path = posixpath.join(data_ingestion,"test.csv")

# s3cilent.s3_client.upload_file(r"C:\Users\Prashant kumar singh\Desktop\US_Visa_verification\artifact\US_VISA\2025-04-30-17-06-57\data_ingestion\RAW_FILE\US_VISA.csv",
#                                Bucket=Bucket_name,Key=s3_file_path)










OBJ = TrainPipeline()

OBJ.run_pipeline()

# from ModelFactory import ModelFactory
# from us_visa.utils.main_utils import *
# from from_root import from_root
# import importlib
# from pyexpat import model

# model_config_path = os.path.join(from_root(),'config','model.yaml')


# train_numpy = r"C:\Users\Prashant kumar singh\Desktop\US_Visa_verification\artifact\US_VISA\2025-04-30-17-06-57\transformed\Train.npy"

# train_array=load_numpy_array_data(train_numpy)
# df=pd.DataFrame(train_array)
# X=df.drop(columns=[24],axis=1)

# Y=df[24]


# m = ModelFactory(model_config_path)

# result=m.best_score(X,Y)



