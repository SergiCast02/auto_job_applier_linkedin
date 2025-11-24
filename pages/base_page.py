from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger
from utils.element_finder import ElementFinder

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.finder = ElementFinder(driver)
    
    def wait_for_dom_ready(self):
        """Espera a DOMContentLoaded usando JavaScript"""
        try:
            self.driver.execute_script("""
                return new Promise(resolve => {
                    if (document.readyState === 'complete') {
                        resolve(true);
                    } else {
                        document.addEventListener('DOMContentLoaded', () => resolve(true));
                    }
                });
            """)
        except:
            pass
    
    def navigate_to(self, url):
        """Navegación ultrarrápida"""
        self.driver.get(url)
        self.wait_for_dom_ready()
        return self
    
    def get_current_url(self):
        return self.driver.current_url
    
    def safe_find_element(self, selector, description=""):
        """Método seguro para encontrar elementos"""
        return self.finder.find_element(selector, description=description)
    
    def safe_click(self, selector, description=""):
        """Método seguro para hacer clic"""
        return self.finder.safe_click(selector, description=description)
    
    def safe_send_keys(self, selector, text, description=""):
        """Método seguro para enviar texto"""
        return self.finder.safe_send_keys(selector, text, description=description)
    
    def is_element_present(self, selector):
        """Verifica si un elemento está presente"""
        return self.finder.is_element_present(selector)