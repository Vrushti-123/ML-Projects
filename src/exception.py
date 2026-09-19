import sys # helps in manipulation of the python runtime environment.
from src.logger import logging

def error_message_detail(error,error_detail:sys): #error_detail --> will be present inside of sys
    _,_,exc_tb=error_detail.exc_info()
    # this will give us three infos: 
    # we are interested in only the third info -->  on which file/which line the exception has occured and everything
    # it'll be stored in exc_tb.

    file_name=exc_tb.tb_frame.f_code.co_filename
    # this is given in custom exception handling documentation.

    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message
# whenever error is raised --> we'll call this function.
    

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    


        