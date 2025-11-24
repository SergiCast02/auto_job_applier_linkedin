from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.logger import logger

class ElementFinder:
    """
    Clase para encontrar y accionar elementos con logging bonito y diferenciado.
    
    Logs generados:
    1. 🔎 BUSCANDO ELEMENTO
    2. ✓ ELEMENTO ENCONTRADO
    3. Acciones diferenciadas:
       - 👆 ACCIÓN → CLICK
       - ⌨️ ACCIÓN → ESCRIBIR
       - 🧹 ACCIÓN → LIMPIAR
       - 📤 ACCIÓN → SUBMIT
    """
    
    def __init__(self, driver):
        self.driver = driver
    
    def find_element(self, selector, timeout=3, description=""):
        """
        Encuentra un elemento de forma segura.
        Logs: 
        1. 🔎 BUSCANDO ELEMENTO
        2. ✓ ELEMENTO ENCONTRADO (si lo encuentra)
        """
        logger.searching_element(selector, description)
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            logger.element_found(selector, description)
            return element
        except TimeoutException:
            # No encontrado - no se registra
            return None
        except Exception as e:
            return None
    
    def find_clickable(self, selector, timeout=5, description=""):
        """
        Encuentra un elemento clickable de forma segura.
        Logs:
        1. 🔎 BUSCANDO ELEMENTO
        2. ✓ ELEMENTO ENCONTRADO (si lo encuentra)
        """
        logger.searching_element(selector, f"{description} (clickable)")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            logger.element_found(selector, f"{description} (clickable)")
            return element
        except TimeoutException:
            return None
        except Exception as e:
            return None
    
    def find_multiple(self, selector, timeout=3, description=""):
        """
        Encuentra múltiples elementos de forma segura.
        Logs:
        1. 🔎 BUSCANDO ELEMENTO
        2. ✓ ELEMENTO ENCONTRADO (si los encuentra)
        """
        logger.searching_element(selector, f"{description} (múltiples)")
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            logger.element_found(selector, f"{description} (encontrados: {len(elements)})")
            return elements
        except TimeoutException:
            return []
        except Exception as e:
            return []
    
    def is_element_present(self, selector, timeout=2):
        """
        Verifica si un elemento está presente SIN logging.
        Método auxiliar interno.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except:
            return False
    
    def safe_click(self, selector, description="", timeout=5):
        """
        Hace clic de forma segura en un elemento.
        
        Logs:
        1. 🔎 BUSCANDO ELEMENTO
        2. ✓ ELEMENTO ENCONTRADO
        3. 👆 ACCIÓN → CLICK
        """
        element = self.find_clickable(selector, timeout, description)
        if element:
            try:
                element.click()
                logger.action_click(description or selector)
                return True
            except Exception as e:
                return False
        return False
    
    def safe_send_keys(self, selector, text, description="", timeout=5, clear_first=True):
        """
        Envía texto de forma segura a un elemento.
        
        Logs:
        1. 🔎 BUSCANDO ELEMENTO
        2. ✓ ELEMENTO ENCONTRADO
        3. 🧹 ACCIÓN → LIMPIAR (si clear_first=True)
        4. ⌨️ ACCIÓN → ESCRIBIR
        """
        element = self.find_element(selector, timeout, description)
        if element:
            try:
                if clear_first:
                    element.clear()
                    logger.action_clear(description or selector)
                
                element.send_keys(text)
                logger.action_send_keys(description or selector, text)
                return True
            except Exception as e:
                return False
        return False
    
    def safe_submit(self, selector, description="", timeout=5):
        """
        Envía un formulario (submit) de forma segura.
        
        Logs:
        1. 🔎 BUSCANDO ELEMENTO
        2. ✓ ELEMENTO ENCONTRADO
        3. 📤 ACCIÓN → SUBMIT
        """
        element = self.find_element(selector, timeout, description)
        if element:
            try:
                element.submit()
                logger.action_submit(description or selector)
                return True
            except Exception as e:
                return False
        return False