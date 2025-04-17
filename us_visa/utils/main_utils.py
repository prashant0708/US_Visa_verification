import os
import sys
import numpy as np
import dill
import yaml
import pandas as pd

from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION

### READ_YAMLFILE FUNCTION 

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
def write_yaml_file()
