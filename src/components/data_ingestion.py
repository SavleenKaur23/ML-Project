import os 
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split

from dataclasses import dataclass
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

@dataclass  # decorator; defines class variables directly, and it auto-generates the __init__ and other methods for us
class DataIngestionConfig:  # any i/p required, we'll give through DataIngestionConfig
    # Inputs are provided to the data ingestion component, enabling it to determine where to store the training and testing data paths.
    train_data_path: str=os.path.join('artifacts','train.csv') # artifact folder(given as input here) to save the data ingestion output 
    test_data_path: str=os.path.join('artifacts','test.csv')
    raw_data_path: str=os.path.join('artifacts','data.csv')

# If a class only contains variables, prefer using the @dataclass decorator;
# if it includes additional methods, use a manual __init__ instead.

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()  # the above 3 variables will get stored as sub objects here
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv('notebook\data\student_perf.csv')  # read from csv, database, api
            logging.info('Read the dataset as dataframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)  #raw data path
            
            logging.info("Train Test Split initiated")  #can be written in utils.py as its a common functionality and called here
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42) 
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)  # train data path
            
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)  # test data path
            
            logging.info("Data Ingestion is completed")
            
            return(       # will be useful in data_transformation
                self.ingestion_config.train_data_path, 
                self.ingestion_config.test_data_path,
                # self.ingestion_config.raw_data_path
                )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()  # create an instance obj of the DataIngestion class.
    train_data, test_data = obj.initiate_data_ingestion() # call the method initiate_data_ingestion() on that instance, which triggers the data ingestion process
    
    data_transformation=DataTransformation()
    train_arr, test_arr, _ =  data_transformation.initiate_data_transformation(train_data,test_data) 
    #train_arr, test_arr, _ : last one not required as we have already created pickle file
    #data_transformation.initiate_data_transformation(train_data,test_data)    

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
    
             # pip install psycopg2-binary sqlalchemy

            # from sqlalchemy import create_engine

            # db_url = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
            # engine = create_engine(db_url)
            # query = "SELECT * FROM sch.student_perf"  #schema.table_name
            # df = pd.read_sql(query, con=engine)

            # logging.info('Read the dataset from PostgreSQL into a dataframe')
            # train_set.to_sql("train_table", con=engine, if_exists='replace', index=False)
            # test_set.to_sql("test_table", con=engine, if_exists='replace', index=False)

