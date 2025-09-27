from app.helpers.selenium_helper import SeleniumHelper
import os

class WorkanaService:
    def __init__(self, selenium_helper: SeleniumHelper):
        self.selenium_helper = selenium_helper
        
    def navigate_to_freelancer_jobs_page(self):
        self.selenium_helper.open_url(os.getenv("URL_WORKANA"))
        
    def wait_page_loaded(self):
        pass