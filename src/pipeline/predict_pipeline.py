import sys
import pandas as pd

from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

class CustomData: #maps the inputs given in home.html to backend with these values
    def __init__(self,
                gender: str,
                race_ethnicity: str,
                parental_level_of_education, 
                lunch: str, 
                test_preparation_course: str,
                reading_score: int, 
                writing_score: int):