import pickle
import os
from selenium.webdriver.remote.webdriver import WebDriver
from config.settings import settings
from utils.logger import logger

class SessionManager:
    def __init__(self):
        self.cookies_file = settings.COOKIES_FILE
        self._ensure_cookies_directory()
    
    def _ensure_cookies_directory(self):
        os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
    
    def save_cookies(self, driver: WebDriver):
        try:
            driver.get("https://www.linkedin.com")
            cookies = driver.get_cookies()
            with open(self.cookies_file, 'wb') as file:
                pickle.dump(cookies, file)
            logger.success("Cookies guardadas")
            return True
        except Exception as e:
            logger.error(f"Error guardando cookies: {e}")
            return False
    
    def load_cookies(self, driver: WebDriver):
        try:
            if not os.path.exists(self.cookies_file):
                logger.debug("No hay cookies guardadas")
                return False
            
            with open(self.cookies_file, 'rb') as file:
                cookies = pickle.load(file)
            
            driver.get("https://www.linkedin.com")
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except:
                    continue
            
            logger.success("Cookies cargadas")
            return True
        except Exception as e:
            logger.error(f"Error cargando cookies: {e}")
            return False
    
    def cookies_exist(self):
        return os.path.exists(self.cookies_file)
    
    def delete_cookies(self):
        try:
            if os.path.exists(self.cookies_file):
                os.remove(self.cookies_file)
                logger.info("Cookies eliminadas")
            return True
        except Exception as e:
            logger.error(f"Error eliminando cookies: {e}")
            return False