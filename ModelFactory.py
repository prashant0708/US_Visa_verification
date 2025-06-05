import sys
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from from_root import from_root
import importlib
from pyexpat import model
from us_visa.utils.main_utils import *
from dataclasses import dataclass
import mlflow
import mlflow.sklearn


GRID_SEARCH_KEY = 'grid_search'
MODULE = 'module'
CLASS = "class"
GRID_SEARCH_PARAM = "params"
MODEL_SELECTION_KEY = 'model_selection'
MODEL_PARAM = "params"
MODEL_SEARCH_PARAM = "search_param_grid"

@dataclass
class InitializedModelDetail:
    model_serial_number:str
    model_name :str
    model : object
    param_grid_search :dict

@dataclass
class GridSearchBestModel:
    model_serial_number:str
    model:str
    best_model:str
    best_parameters:str
    best_score:str



def class_import(module,class_name):
    try:
        module = importlib.import_module(module)
        model_class = getattr(module,class_name)
        class_ref = model_class
        return class_ref
    except Exception as e:
        raise(sys,e)
    
def update_property_class(class_inst:object,property_data:dict):
    try:
        for key,value in property_data.items():
            setattr(class_inst,key,value)
        return class_inst
    except Exception as e:
        raise(sys,e)

class ModelFactory:
    def __init__(self,model_config_path:str):
        self.model_config_path = read_yaml_file(model_config_path)
        self.grid_config_path = read_yaml_file(model_config_path)

    def model_intilization_list(self):
        try:
            model_config = self.model_config_path
            models_initialization_config = model_config[MODEL_SELECTION_KEY]
            model_list=[]
            for model_serical_number in models_initialization_config.keys():
                module_name = models_initialization_config[model_serical_number][MODULE]
                class_name = models_initialization_config[ model_serical_number][CLASS]
                
                class_ref = class_import(module_name,class_name)
                models= class_ref()
            
                if MODEL_PARAM in models_initialization_config[model_serical_number]:
                    model_obj_property_data = dict(models_initialization_config[model_serical_number][MODEL_PARAM])
                    models = update_property_class(class_inst=models,property_data=model_obj_property_data)

                param_grid_search = models_initialization_config[model_serical_number][MODEL_SEARCH_PARAM]
                model_name = f"{class_name}"
                model_detais = InitializedModelDetail(model_serial_number=model_serical_number,
                                                    model_name=model_name,
                                                    model=models,
                                                    param_grid_search=param_grid_search)
                
                model_list.append(model_detais)
            return model_list
        except Exception as e:
            raise(sys,e)
    def execute_grid_search_operation(self,model_list:InitializedModelDetail,
                                      input_feature,output_feature)->GridSearchBestModel:
        try:
            Grid_config = self.grid_config_path
            grid_module = Grid_config[GRID_SEARCH_KEY][MODULE]
            grid_class = Grid_config[GRID_SEARCH_KEY][CLASS]
            grid_param = Grid_config[GRID_SEARCH_KEY][GRID_SEARCH_PARAM]
            grid_search_cv_ref = class_import(grid_module,grid_class)
            grid_search_cv = grid_search_cv_ref(estimator=model_list.model,
                                                param_grid=model_list.param_grid_search)
            
            grid_search_cv = update_property_class(grid_search_cv,property_data=grid_param)

            grid_search_cv.fit(input_feature,output_feature)

            



            grid_searches_best_model = GridSearchBestModel(model_serial_number=model_list.model_serial_number,
                                                        model=model_list.model_name,
                                                        best_model=grid_search_cv.best_estimator_,
                                                        best_parameters=grid_search_cv.best_params_,
                                                        best_score=grid_search_cv.best_score_)
            return grid_searches_best_model
        except Exception as e:
            raise(sys,e)
    
    def initiate_grid_search_cv(self,inputs , output):
        try:

            model_list = self.model_intilization_list()
            for model_details in model_list:
                grid_search_artifact =self.execute_grid_search_operation(model_list=model_details,
                                            input_feature=inputs,
                                            output_feature=output)   
            return grid_search_artifact
        except Exception as e:
            raise(sys,e)
    def best_score(self,X,Y,best_score=1):
        try:
            result= self.initiate_grid_search_cv(inputs=X,output=Y)
            
            if result.best_score>=best_score:
                return result
            else:
                print("No Model found to meet the best score")
                logging.info("No Model found to meet the best score")
        except Exception as e:
           raise(sys,e)
        




        

        
            




        






