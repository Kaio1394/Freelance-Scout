from app.helpers.selenium_helper import SeleniumHelper
from app.core.config_loader import SELECTORS, VARIABLES
from app.schemas.freelancer_schema import FreelancerBase
import itertools


class WorkanaService:
    def __init__(self, selenium_helper: SeleniumHelper):
        self.selenium_helper = selenium_helper
        
    def navigate_to_freelancer_jobs_page(self):
        self.selenium_helper.open_url(VARIABLES["workana"]["url"])
        self.selenium_helper.wait_element("xpath", SELECTORS["workana"]["search_input"])
        
    def div_cookies_exist(self):
        element = self.selenium_helper.wait_element("xpath", SELECTORS['workana']['div_cookies'])
        if element is None:
            return False
        return True
    
    def click_accept_cookies(self):
        self.selenium_helper.click("xpath", SELECTORS["workana"]["accept_cookies"])
        
    def set_text_search_job(self, text_job: str):
        self.selenium_helper.set_text("xpath", SELECTORS["workana"]["search_input"], text_job)
        
    def click_seach_job(self):
        self.selenium_helper.click("xpath", SELECTORS["workana"]["search_button"])
        
    def empty_search(self) -> bool:
        element = self.selenium_helper.wait_element("xpath", str(SELECTORS['workana']['empty_search']))
        if element is None:
            return False
        return True
    
    def get_text_empty_search(self) -> str:
        return self.selenium_helper.get_text("xpath", SELECTORS['workana']['empty_search_text'])
        
    def card_job_exist(self, index: int) -> bool:
        selector: str = SELECTORS['workana']['project_item']
        selector = selector.replace('INDEX_PROJECT', f'{str(index)}')
        element = self.selenium_helper.wait_element("xpath", selector)
        if element is None:
            return False
        return True
    
    def get_all_jobs(self) -> list[FreelancerBase]:
        list_jobs: list[FreelancerBase] = []
        try:           
            for i in itertools.count():
                title = self.get_attribute_project("title", i + 1),
                about = self.get_attribute_project("about", i + 1),
                author = self.get_attribute_project("author", i + 1),
                budget = self.get_attribute_project("budget", i + 1),
                stars = self.get_attribute_project("stars", i + 1),
                skills=self.get_attribute_project("skills", i + 1) or []
                
                freelancer = FreelancerBase(title, about, author, budget, stars, skills)
                list_jobs.append(freelancer)
            return list_jobs
        except Exception:
            if len(list_jobs) == 0:
                raise Exception("")
            return list_jobs        
    
    def get_attribute_project(self, attribute: str, index) -> str:
        selector: str
        text: str
        match attribute.lower().strip():
            case "author":
                selector = SELECTORS['workana']['project_author']
            case "title":
                selector = SELECTORS['workana']['project_title']
            case "budget":
                selector = SELECTORS['workana']['project_budget']
            case "about":
                selector = SELECTORS['workana']['project_about']
            case "stars":
                selector = SELECTORS['workana']['project_profile_star']
            case _:
                raise ValueError("Value invalid.")
        selector = selector.replace('INDEX_PROJECT', f'{str(index)}')
        if attribute == "stars":
            text = self.selenium_helper.get_attribute("xpath", selector, "title")
        else:
            text = self.selenium_helper.get_text("xpath", selector)
        return text