from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger
from utils.element_finder import ElementFinder

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.finder = ElementFinder(driver)
    
    def wait_for_dom_ready(self):
        """Espera a DOMContentLoaded usando JavaScript y hace log"""
        try:
            logger.debug("Esperando DOMContentLoaded...")
            self.driver.execute_script("""
                return new Promise(resolve => {
                    if (document.readyState === 'complete') {
                        resolve(true);
                    } else {
                        document.addEventListener('DOMContentLoaded', () => resolve(true));
                    }
                });
            """)
            logger.success("DOMContentLoaded completado")
            return True
        except Exception as e:
            logger.warning(f"DOMContentLoaded no se pudo verificar: {e}")
            return False
    
    def navigate_to(self, url):
        """Navegación con log de DOMContentLoaded"""
        logger.debug(f"Navegando a: {url}")
        self.driver.get(url)
        self.wait_for_dom_ready()
        return self
    
    def get_current_url(self):
        return self.driver.current_url
    
    def safe_find_element(self, selector, description=""):
        return self.finder.find_element(selector, description=description)
    
    def safe_click(self, selector, description=""):
        return self.finder.safe_click(selector, description=description)
    
    def safe_send_keys(self, selector, text, description=""):
        return self.finder.safe_send_keys(selector, text, description=description)
    
    def is_element_present(self, selector):
        return self.finder.is_element_present(selector)