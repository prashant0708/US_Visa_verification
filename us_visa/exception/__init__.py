import os 
import sys
def error_message_details(error,error_detail:sys):
    _,_,exc_tb=sys.exc_info()
    file_name= exc_tb.tb_frame.f_code.co_filename
    exception_block_line_number = exc_tb.tb_frame.f_lineno
    try_block_line_number = exc_tb.tb_lineno
    
    error_message = f"""
    Error occuredin python script: [{file_name}] at try block line number : [{try_block_line_number}]  and exception block line number : [{exception_block_line_number},*****[{str(error)}]]
    """
    
    return error_message


class USVISAEXCEPTION(Exception):  ##USVISAEXCEPTION got all the build in functionality of Exception 
    def __init__(self,error_message,error_details:sys):
        """

        Args:
            error_message (string): 
            error_details (_type_): sys
        """
        
        super().__init__(error_message)  # Calls Exception's constructor when this line run The built-in Exception class stores error_message internally.
        self.error_message = error_message_details(error_message,error_detail=error_details) ## edit the error message with custom details message and passed to self.error_message
        
    def __str__(self):
        return self.error_message
    
    
"""
super().__init__(error_message) stores the original error message inside the base Exception class.

The Exception class uses this message when printing or logging errors.

self.error_message = error_message_details(...) replaces it with a more detailed version.

When print(my_exception) is called, it prints self.error_message, not the original one.
"""
       