import os 
import pandas as pd
from pandas import DataFrame

class ExcelHelper:
    def __init__(self):
        self.__path_file = None
        self.__tab = None
    
    def set_path_file(self, path: str):
        self.__path_file = path

    def set_tab(self, tab: str):
        self.__tab = tab
        
    def exists(self) -> bool:
        return os.path.isfile(self.__path_file)
    
    def spreadsheet_to_dataframe(self) -> DataFrame:
        return pd.read_excel(io=self.__path_file, sheet_name=self.__tab)
        
    def dataframe_to_spreadsheet(self):
        pass
    