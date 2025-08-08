import os
import sys

import pandas as pd
import numpy as np
import dill  # dill lets you save almost any Python object to a file, and load it later
from src.exception import CustomException

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score

#can add train_test_split from data ingestion.py here and call in data ingestion

def save_object(file_path, obj):  #saves any Python object to a given file path using dill

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, "wb") as file_obj:  #opens the file in write-binary mode
            dill.dump(obj,file_obj)  #works like pickle.dump() but supports more complex Python objects (like lambdas, closures, etc.).

    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train,y_train, X_test, y_test, models, model_params):
    try:
     #   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, randome_state =42)
        report = {}

        for i in range(len(list(models))):  
            model = list(models.values())[i] #value of each model
            para = model_params[list(models.keys())[i]]
            
            gcv = GridSearchCV(model, para, cv = 3)
            gcv.fit(X_train,y_train)
            
            model.set_params(**gcv.best_params_)
            model.fit(X_train, y_train)

            y_train_predict = model.predict(X_train)
            y_test_predict = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_predict)
            test_model_score = r2_score(y_test, y_test_predict)

            report[list(models.keys())[i]] = test_model_score
        
        return report

    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try: 
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)