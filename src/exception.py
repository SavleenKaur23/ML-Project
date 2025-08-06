# refer https://docs.python.org/3/library/exceptions.html and https://docs.python.org/3/tutorial/errors.html
import sys 
from logger import logging # logging setup file is logger.py

# custom message for an exception
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info() #first two information are not required , we only want to see exc_tb i.e. which file, line number the exception has occurred
    file_name = exc_tb.tb_frame.f_code.co_filename #exc_tb.tb_frame.f_code.co_filename accesses the file name where the error occurred by navigating from the exception traceback (exc_tb),
    #to the frame of code running when the error happened (tb_frame), to the code object (f_code), and finally to the filename (co_filename) where that code is defined.
    error_message="Error occurred in Python Script name [{0}] and line number [{1}] with error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))
    return error_message
    

class CustomException(Exception): # (1)custom error class called CustomException  (2) inherits from Python’s built-in Exception class
    def __init__(self, error_message, error_detail:sys):  # __init__ :constructor  (takes 2 inputs here)
        #self: current instance of the class and used to store data in the object being created
        super().__init__(error_message) # calls the parent class (Exception) constructor
        self.error_message=error_message_detail(error_message,error_detail=error_detail) #(1)helper function error_message_detail() to build a full, detailed error string (2)storing it in self.error_message so it can be used later

    def __str__(self):
        return self.error_message # when you print the exception, this will be shown
    
# whenever we get an exception, we'll take the exception and log it with the logger file and use logging.info to put it inside the file

# Testing of exception.py ie. if the  exceptions in the logs are getting recorded 
# if __name__=='__main__':
#     try:
#         a=1/0
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True) ## log the traceback and error here
#         #logging.info("Divide by zero")
#         raise CustomException(e,sys) 