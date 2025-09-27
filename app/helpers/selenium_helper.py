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
from selenium import Web

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
                opts.add_argument("--disable-gpu")
                opts.add_argument("--no-sandbox")
            if self.user_agent:
                opts.add_argument(f"user-agent={self.user_agent}")
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=opts)
        
    def open_url(self, url: str):
        self.driver.get(url)
        
    def wait_element(self, by: By, selector: str, timeout: float = 5.0) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
        
    def get_title(self):
        return self.driver.title
    
    def quit(self):
        try:
            self.driver.close()
        except Exception:
            pass