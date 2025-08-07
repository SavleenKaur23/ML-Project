import os
import sys

import pandas as pd
import numpy as np
import dill  # dill lets you save almost any Python object to a file, and load it later
from src.exception import CustomException

#can add train_test_split from data ingestion.py here and call in data ingestion

def save_object(file_path, obj):  #saves any Python object to a given file path using dill

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, "wb") as file_obj:  #opens the file in write-binary mode
            dill.dump(obj,file_obj)  #works like pickle.dump() but supports more complex Python objects (like lambdas, closures, etc.).

    except Exception as e:
        raise CustomException(e,sys)