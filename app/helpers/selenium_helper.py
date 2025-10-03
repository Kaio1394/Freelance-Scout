from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

class SeleniumHelper:
    def __init__(self, browser: str = "chrome", headless: bool = True, user_agent: str | None = None):
        self.browser = browser.lower()
        self.headless = headless
        self.user_agent = user_agent
        self.driver = self._create_driver()
        
    def _create_driver(self):
        if self.browser == "chrome":
            opts = ChromeOptions()
            if self.headless:
                opts.add_argument("--headless=new")
                opts.add_argument("--window-size=1920,1080")
                opts.add_argument("--disable-gpu")
                opts.add_argument("--no-sandbox")
            if self.user_agent:
                opts.add_argument(f"user-agent={self.user_agent}")
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=opts)
        
    def open_url(self, url: str):
        self.driver.get(url)
        
    def wait_element(self, by: str, selector: str, timeout: float = 5.0) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((self._get_by(by), selector))
            )
        except Exception:
            return None
    
        
    def get_title(self):
        return self.driver.title
    
    def quit(self):
        try:
            self.driver.close()
        except Exception:
            pass
        
    def get_attribute(self, by: str, selector: str, attribute: str):
        return self.driver.find_element(self._get_by(by), selector).get_attribute(attribute)
        
    def get_text(self, by: str, selector: str) -> str:
        try:
            return self.driver.find_element(self._get_by(by), selector).text
        except Exception:
            return ""
        
    def click(self, by: str, selector: str):
        self.wait_element(by, selector).click()
    
    def set_text(self, by: str, selector: str, text: str, keystrokes_delays: bool = False, delay: float = 1.0):
        if keystrokes_delays:
            for char in text:
                self.wait_element(by, selector).send_keys(char)
                time.sleep(delay)
        else:
            self.wait_element(by, selector).send_keys(text)
        
    def _get_by(self, by: str) -> By:
        match by.lower().strip():
            case "id":
                return By.ID
            case "xpath":
                return By.XPATH
            case "class":
                return By.CLASS_NAME
            case "name":
                return By.NAME
            case "tag_name":
                return By.TAG_NAME
            case _:
                raise ValueError("Type of By invalid.")