from fastapi import Depends
from app.helpers.selenium_helper import SeleniumHelper
from app.services.workana_service import WorkanaService
from typing import Generator
from app.helpers.email_helper import EmailHelper
from app.services.email_service import EmailService
from app.helpers.excel_helper import ExcelHelper
from app.services.excel_service import ExcelService

def get_selenium_helper() -> Generator[SeleniumHelper, None, None]:
    helper = SeleniumHelper(headless=True)
    try:
        yield helper
    finally:
        helper.quit()
        
def get_email_helper() -> Generator[EmailHelper, None, None]:
    email = EmailHelper()
    try:
        yield email
    finally:
        email.disconnect()
        
def get_excel_helper() -> Generator[EmailHelper, None, None]:
    excel = ExcelHelper()
    return excel
        
def get_email_service(helper: EmailHelper = Depends(get_email_helper)) -> EmailService:
    return EmailService(email_helper=helper)

def get_workana_service(helper: SeleniumHelper = Depends(get_selenium_helper)) -> WorkanaService:
    return WorkanaService(selenium_helper=helper)

def get_excel_service(helper: ExcelHelper = Depends(get_excel_helper)) -> ExcelService:
    return ExcelService(helper)