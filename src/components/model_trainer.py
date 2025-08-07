import os
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
#from src.components.data_ingestion import DataIngestionConfig, DataIngestion # may cause loop
#from src.components.data_transformation import DataTransformationConfig, DataTransformation  may cause loop
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model

import pandas as pd
import numpy as np 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_arr,test_arr):  #train_arr,test_arr from data transformation
        try:
            logging.info("Split train and test input data")
            X_train, y_train,X_test,y_test = (
                train_arr[:,:-1], 
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "DecisionTreeRegressor": DecisionTreeRegressor(),
                "AdaBoostRegressor": AdaBoostRegressor(),
                "XGBRegressor": XGBRegressor(),
                "GradientBoostingRegressor": GradientBoostingRegressor(),
                "LinearRegression": LinearRegression(),
                "CatBoostRegressor": CatBoostRegressor(verbose=False),
                "KNeighborsRegressor": KNeighborsRegressor()
            }
        
            model_report:dict=evaluate_model(X_train=X_train, y_train=y_train,X_test=X_test, y_test=y_test,
                                          models = models)        

            # To get the best model score
            best_model_score = max(sorted(model_report.values()))   

            # Fetch the name of best model
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]  

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("Tune the models or try another model to find the best model")
            logging.info(f"Best Model found")

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)
            
            r2_square = r2_score(y_test, predicted)
            return round(r2_square, 2)
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
