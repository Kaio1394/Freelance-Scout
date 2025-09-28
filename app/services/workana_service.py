from app.helpers.selenium_helper import SeleniumHelper
from app.core.config_loader import SELECTORS, VARIABLES

class WorkanaService:
    def __init__(self, selenium_helper: SeleniumHelper):
        self.selenium_helper = selenium_helper
        
    def navigate_to_freelancer_jobs_page(self):
        self.selenium_helper.open_url(VARIABLES["workana"]["url"])
        self.selenium_helper.wait_element("xpath", SELECTORS["workana"]["search_input"])
        
    def wait_page_loaded(self):
        pass