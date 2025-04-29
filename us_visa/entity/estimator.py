import pandas as pd
import sys
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION




class TargetValueMapping:
    def __init__(self):
        self.Certified :int = 1
        self.Denied:int = 0

    def asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        reverse_mapping_value = self.asdict()
        return dict(zip(reverse_mapping_value.values(),reverse_mapping_value.keys()))
