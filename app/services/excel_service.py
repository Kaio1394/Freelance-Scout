from app.helpers.excel_helper import ExcelHelper

class ExcelService:
    def __init__(self, helper: ExcelHelper):
       self.helper = helper
       
    def get_dataframe(self, path: str, tab: str):
        self.helper.set_path_file(path)
        self.helper.set_tab(tab)
        if not self.helper.exists():
            raise FileNotFoundError(f"File xlsx [{path}] not found.")
        return self.helper.spreadsheet_to_dataframe()