from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.logger import logger

class ElementFinder:
    def __init__(self, driver):
        self.driver = driver
    
    def find_element(self, selector, timeout=3, description=""):
        """Encuentra un elemento de forma segura sin crashear"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            logger.debug(f"Elemento encontrado: {description} -> {selector}")
            return element
        except TimeoutException:
            logger.warning(f"Elemento NO encontrado: {description} -> {selector}")
            return None
        except Exception as e:
            logger.error(f"Error buscando elemento {description}: {e}")
            return None
    
    def find_clickable(self, selector, timeout=5, description=""):
        """Encuentra un elemento clickable de forma segura"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            logger.debug(f"Elemento clickable encontrado: {description} -> {selector}")
            return element
        except TimeoutException:
            logger.warning(f"Elemento clickable NO encontrado: {description} -> {selector}")
            return None
        except Exception as e:
            logger.error(f"Error buscando elemento clickable {description}: {e}")
            return None
    
    def find_multiple(self, selector, timeout=3, description=""):
        """Encuentra múltiples elementos de forma segura"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            logger.debug(f"Encontrados {len(elements)} elementos: {description} -> {selector}")
            return elements
        except TimeoutException:
            logger.warning(f"No se encontraron elementos: {description} -> {selector}")
            return []
        except Exception as e:
            logger.error(f"Error buscando múltiples elementos {description}: {e}")
            return []
    
    def is_element_present(self, selector, timeout=2):
        """Verifica si un elemento está presente sin lanzar excepciones"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except:
            return False
    
    def safe_click(self, selector, description="", timeout=5):
        """Hace clic de forma segura en un elemento"""
        element = self.find_clickable(selector, timeout, description)
        if element:
            try:
                element.click()
                logger.debug(f"Clic exitoso en: {description}")
                return True
            except Exception as e:
                logger.error(f"Error haciendo clic en {description}: {e}")
                return False
        return False
    
    def safe_send_keys(self, selector, text, description="", timeout=5):
        """Envía texto de forma segura a un elemento"""
        element = self.find_element(selector, timeout, description)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                logger.debug(f"Texto enviado a {description}: {text[:10]}...")
                return True
            except Exception as e:
                logger.error(f"Error enviando texto a {description}: {e}")
                return False
        return False