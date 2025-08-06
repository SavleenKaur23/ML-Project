#Logging in a text file

import logging
import os
from datetime import datetime

logs_path=os.path.join(os.getcwd(),"logs") 
os.makedirs(logs_path,exist_ok=True) #Creates folder 'logs' if it doesn't exist

LOG_FILE="app.logs"
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE) # full file path for your log file inside the logs folder

#LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
#logs_path=os.path.join(os.getcwd(),"logs")
#os.makedirs(logs_path,exist_ok=True) #Creates folder 'logs' if it doesn't exist

#LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE) # full file path for your log file inside the logs folder

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] - %(lineno)d - %(levelname)s - %(name)s - %(message)s',
             #controls how each log message looks :Timestamp, log level , module name, error message
    level = logging.INFO # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)

# Testing of logger.py ie. if the logs are getting recorded
# if __name__=='__main__':
#     logging.info("Logging has started")