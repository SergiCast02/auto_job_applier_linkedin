from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger
from utils.element_finder import ElementFinder

class BasePage:
    """
    Clase base para todas las páginas.
    Implementa navegación y búsqueda de elementos con logging modularizado.
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.finder = ElementFinder(driver)
    
    def wait_for_dom_ready(self):
        """
        Paso 1: Espera a que la página cargue COMPLETAMENTE (incluyendo recursos)
        Log: PAGINA CARGO COMPLETAMENTE (DOMContentLoaded)
        """
        import time
        try:
            # Esperar a que el documento esté completo
            self.driver.execute_script("""
                return new Promise(resolve => {
                    if (document.readyState === 'complete') {
                        resolve(true);
                    } else {
                        window.addEventListener('load', () => resolve(true));
                    }
                });
            """)
            
            # Espera adicional para recursos asíncronos (imágenes, CSS, fuentes)
            # LinkedIn carga muchos recursos de forma asíncrona
            time.sleep(2)
            
            # Verificar que jQuery esté cargado (LinkedIn lo usa)
            try:
                self.driver.execute_script("return typeof jQuery !== 'undefined'")
            except:
                pass
            
            logger.page_loaded(self.driver.current_url)
            return True
        except Exception as e:
            return False
    
    def navigate_to(self, url):
        """
        Navegación con logs modularizados:
        1. URL de la pagina
        2. PAGINA CARGO COMPLETAMENTE
        """
        self.driver.get(url)
        logger.current_url(url)
        self.wait_for_dom_ready()
        return self
    
    def get_current_url(self):
        """Obtiene la URL actual sin logging"""
        return self.driver.current_url
    
    def safe_find_element(self, selector, description=""):
        """
        Busca elemento con log:
        - ELEMENTO ENCONTRADO: selector - description
        """
        return self.finder.find_element(selector, description=description)
    
    def safe_click(self, selector, description=""):
        """
        Click con logs:
        1. ELEMENTO ENCONTRADO
        2. ELEMENTO ACCIONADO: description - click
        """
        return self.finder.safe_click(selector, description=description)
    
    def safe_send_keys(self, selector, text, description=""):
        """
        Enviar texto con logs:
        1. ELEMENTO ENCONTRADO
        2. ELEMENTO ACCIONADO: description - send_keys
        """
        return self.finder.safe_send_keys(selector, text, description=description)
    
    def is_element_present(self, selector):
        """Verifica presencia sin logging (método auxiliar)"""
        return self.finder.is_element_present(selector)