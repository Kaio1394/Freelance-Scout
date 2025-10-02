from app.helpers.selenium_helper import SeleniumHelper
from app.core.config_loader import SELECTORS, VARIABLES
from app.schemas.freelancer_schema import FreelancerBase
import itertools
import time

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
    
    def get_count_page_search(self) -> int:
        selector: str
        index_pagination: int
        for index_pagination in itertools.count():
            try:
                if index_pagination == 0:
                    continue
                selector = str(SELECTORS['workana']['button_pagination']).replace("INDEX_PAG", f"{str(index_pagination)}")
                self.selenium_helper.click("xpath", selector)                
                time.sleep(2)
            except Exception:
                break
        self.click_button_pagination_init()
        return index_pagination - 1
    
    def click_button_pagination(self, index: int):
        selector = str(SELECTORS['workana']['button_pagination'])
        self.selenium_helper.click("xpath", selector.replace('INDEX_PAG', f'{str(index)}'))
        
    def click_button_pagination_init(self):
        selector = str(SELECTORS['workana']['button_pagination'])
        self.selenium_helper.click("xpath", selector.replace('INDEX_PAG', 'Início'))
        
    def div_register_exist(self) -> bool:
        selector = SELECTORS['workana']['button_close_register_div']
        element = self.selenium_helper.wait_element("xpath", selector, 1)
        if element is None:
            return False
        return True
    
    def click_close_div_register(self):
        selector: str = SELECTORS['workana']['button_close_register_div']
        self.selenium_helper.click("xpath", selector)
    
    # def div_register_exist(self) -> bool:
    #     selector = SELECTORS['workana']['div_register']
    #     element = self.selenium_helper.wait_element("xpath", selector, 1)
    #     if element is None:
    #         return False
    #     return True
    
    def get_all_jobs(self, limit: int = None) -> list[FreelancerBase]:
        list_jobs: list[FreelancerBase] = []
        counter: int = 1
        stop_exec: bool = False
        if limit <= 0:
            raise ValueError("Limit can't be less or equal than zero.")
        try: 
            # count_pages: int = self.get_count_page_search()
            count_pages: int = 50                  
            for page_count in range(count_pages + 1):
                if stop_exec:
                    break
                if page_count == 0:
                    continue
                for i in itertools.count():
                    if counter > limit:
                        stop_exec = True
                        break
                    try:
                        if i == 0:
                            continue
                        title = self.get_attribute_project("title", i)
                        about = self.get_attribute_project("about", i)
                        author = self.get_attribute_project("author", i)
                        budget = self.get_attribute_project("budget", i)
                        stars = self.get_attribute_project("stars", i)
                        skills = self.get_attribute_project("skills", i) or []                      
                        freelancer = FreelancerBase(
                            title=title,
                            about=about,
                            author=author,
                            budget=budget,
                            stars=stars,
                            skills=skills
                        )
                        list_jobs.append(freelancer)
                        counter += 1
                    except Exception as err:
                        break
                self.click_button_pagination(page_count)
            return list_jobs
        except Exception:
            if len(list_jobs) == 0:
                raise Exception("")
            return list_jobs   
        
    def get_list_skills(self, index: int):
        selector = str(SELECTORS['workana']['project_skills']).replace("INDEX_PROJECT", f"{str(index)}")
        list_skills: list[str] = []
        for index_skill in itertools.count():
            try:
                if index_skill == 0:
                    continue
                selector_skills = selector.replace('INDEX_SKILL', f'{str(index_skill)}')
                text = self.selenium_helper.get_text("xpath", selector_skills)
                if text == '': 
                    raise Exception()
                list_skills.append(text)
            except Exception:
                break
        return list_skills
        
    def get_attribute_project(self, attribute: str, index: int) -> str | list[str]:
        selector: str
        text: str
        list_skills: list[str] = []
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
            case "skills":
                list_skills = self.get_list_skills(index)
                return list_skills
            case _:
                raise ValueError(f"Value '{attribute}' invalid.")
        selector = selector.replace('INDEX_PROJECT', f'{str(index)}')
        if attribute == "stars":
            text = self.selenium_helper.get_attribute("xpath", selector, "title")
        else:
            text = self.selenium_helper.get_text("xpath", selector)
        return text