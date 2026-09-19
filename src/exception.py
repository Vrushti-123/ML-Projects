import sys # helps in manipulation of the python runtime environment.
# sys.exc_info() --> This gives information about the currently handled exception.
from src.logger import logging

def error_message_detail(error,error_detail:sys): #error_detail --> will be present inside of sys --> sys.exc_info()
    _,_,exc_tb=error_detail.exc_info()
    '''
    this will give us three infos: type, value, traceback

    For example:
        exc_type  → ZeroDivisionError
        exc_value → division by zero
        exc_tb    → information about where it happened

        we are interested in only the third info -->  on which file/which line the exception has occured and everything
        it'll be stored in exc_tb.
        
    '''
    
    file_name=exc_tb.tb_frame.f_code.co_filename
    # this is given in custom exception handling documentation.
    # traceback --> Get the frame where the exception occurred --> Get information about the Python code being executed --> Get the filename.
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name, exc_tb.tb_lineno, str(error))

    return error_message
# whenever error is raised --> we'll call this function.
    

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message) #initialize the parent Exception class.
        self.error_message=error_message_detail(
            error_message, #call the function above and get the error msg
            error_detail=error_detail #error detail --> obtained from runtime env --> sys.exc_info()
            )
    
    def __str__(self):
        return self.error_message


'''
This is basically how the error will be passed:

try:
    x = 10 / 0
except Exception as e:
    error = CustomException(e, sys)
    logging.error(error)
    raise error

this code also handles logging of errors :)
'''