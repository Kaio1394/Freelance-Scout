from fastapi import Depends
from app.helpers.selenium_helper import SeleniumHelper
from app.services.workana_service import WorkanaService
from typing import Generator

def get_selenium_helper() -> Generator[SeleniumHelper, None, None]:
    helper = SeleniumHelper(headless=True)
    try:
        yield helper
    finally:
        helper.quit()

def get_workana_service(helper: SeleniumHelper = Depends(get_selenium_helper)) -> WorkanaService:
    return WorkanaService(selenium_helper=helper)