from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact


OBJ = TrainPipeline()

OBJ.run_pipeline()

from ModelFactory import ModelFactory
from us_visa.utils.main_utils import *
from from_root import from_root
import importlib
from pyexpat import model

model_config_path = os.path.join(from_root(),'config','model.yaml')


train_numpy = r"C:\Users\Prashant kumar singh\Desktop\US_Visa_verification\artifact\US_VISA\2025-04-30-17-06-57\transformed\Train.npy"

train_array=load_numpy_array_data(train_numpy)
df=pd.DataFrame(train_array)
X=df.drop(columns=[24],axis=1)

Y=df[24]


m = ModelFactory(model_config_path)

result=m.best_score(X,Y)



