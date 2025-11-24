import pickle
import os
from selenium.webdriver.remote.webdriver import WebDriver
from config.settings import settings

class SessionManager:
    """
    Gestor de sesión para cookies.
    NO genera logs - operaciones internas silenciosas.
    """
    
    def __init__(self):
        self.cookies_file = settings.COOKIES_FILE
        self._ensure_cookies_directory()
    
    def _ensure_cookies_directory(self):
        """Crea directorio de cookies si no existe"""
        os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
    
    def save_cookies(self, driver: WebDriver):
        """
        Guarda cookies del navegador.
        Operación silenciosa - no genera logs.
        """
        try:
            driver.get("https://www.linkedin.com")
            cookies = driver.get_cookies()
            with open(self.cookies_file, 'wb') as file:
                pickle.dump(cookies, file)
            return True
        except Exception as e:
            return False
    
    def load_cookies(self, driver: WebDriver):
        """
        Carga cookies en el navegador.
        Operación silenciosa - no genera logs.
        """
        try:
            if not os.path.exists(self.cookies_file):
                return False
            
            with open(self.cookies_file, 'rb') as file:
                cookies = pickle.load(file)
            
            driver.get("https://www.linkedin.com")
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except:
                    continue
            
            return True
        except Exception as e:
            return False
    
    def cookies_exist(self):
        """
        Verifica si existen cookies guardadas.
        Operación silenciosa - no genera logs.
        """
        return os.path.exists(self.cookies_file)
    
    def delete_cookies(self):
        """
        Elimina cookies guardadas.
        Operación silenciosa - no genera logs.
        """
        try:
            if os.path.exists(self.cookies_file):
                os.remove(self.cookies_file)
            return True
        except Exception as e:
            return False