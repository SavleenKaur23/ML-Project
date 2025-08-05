from setuptools import find_packages,setup
from typing import List
# meta data about our project

HYPHEN_E_DOT="-e ."

def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of required libraries
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines() # using readlines will read /n from requirements.txt i.e /n will get recorded
        requirements=[req.replace("\n","") for req in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)  # as we parse each line of requirements.txt , it should not consider – e . 
    return requirements


setup(
    name='mlproject',
    version='0.0.1',
    author='SK',
    author_email='ksavleends@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements("requirements.txt") #['pandas','numpy','scikit-learn','seaborn',]
)