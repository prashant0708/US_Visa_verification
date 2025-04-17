import os
import sys
import numpy as np
import dill
import yaml
from pandas import DataFrame

from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION

### READ_YAMLFILE FUNCTION 

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
    
## function to write yaml file

def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        
        with open(file_path,"w") as file:
            yaml.dump(content,file)
        logging.info(f"yaml content dump at file location : {file_path}")
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
## function to load the object

def load_object(file_path:str) ->object:
    logging.info("Entered the load_object method of utils")
    
    try:
        with open(file_path,"rb") as file_obj:
            obj = dill.load(file_obj)
        logging.info("Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
###  function save the object
def save_object(file_path:str , obj:object)->None:
    logging.info("Entred the save_object method of utils")
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Object are saved at location: {file_path}")
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
def save_numpy_array_data(file_path:str , array : np.array)->None:
    """ 
    save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok= True)
        
        with open(file_path,"wb") as file_obj:
            np.save(array,file_obj)
        logging.info(f"numpy array data saved at file location : {file_path}")
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
### load the numpy array

def load_numpy_array_data (file_path:str)-> np.array:
    try:
        with open(file_path , 'rb') as file_obj:
            return np.load(file_obj)
        logging.info(f"array data read by np from location {file_path}")
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
## function to drop the columns

def drop_columns(df:DataFrame,cols:list)->DataFrame:
    try:
        df = df.drop(columns=cols,axis=1)
        logging.info("Exited the drop_columns method of utils")
        return df
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    


        
    
    

