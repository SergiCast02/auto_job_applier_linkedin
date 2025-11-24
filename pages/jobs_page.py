from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from config.settings import settings
from utils.logger import logger

class JobsPage(BasePage):
    """
    Página de LinkedIn Jobs con acciones modularizadas.
    Cada método representa un paso claro con logging apropiado.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        # Selectores como constantes
        self.EMAIL_SELECTOR = '[name="session_key"]'
        self.PASSWORD_SELECTOR = '[name="session_password"]'
        self.LOGIN_BUTTON_SELECTOR = '[data-id="sign-in-form__submit-btn"][type="submit"]'
        self.JOBS_INDICATOR = '[placeholder="Title, skill or Company"]'
        self.LOGIN_FORM_SELECTOR = 'form[data-id="sign-in-form"]'
        self.SEARCH_INPUT_SELECTOR = '[placeholder="Title, skill or Company"]'
    
    # ==================== PASO 1: NAVEGACIÓN ====================
    
    def navigate_to_jobs(self):
        """
        Paso 1: Navegar a LinkedIn Jobs
        Logs automáticos:
        - URL: https://www.linkedin.com/jobs/
        - PAGINA CARGO COMPLETAMENTE
        """
        return self.navigate_to("https://www.linkedin.com/jobs/")
    
    # ==================== PASO 2: VERIFICACIONES ====================
    
    def is_login_form_present(self):
        """
        Verificación: detecta si el formulario de login está presente.
        NO genera logs (método interno - usa is_element_present).
        
        Retorna True si encuentra:
        - Formulario de login completo
        - O campos de email + password
        """
        # Verificar formulario completo
        if self.is_element_present(self.LOGIN_FORM_SELECTOR):
            return True
        
        # Verificar campos individuales
        if (self.is_element_present(self.EMAIL_SELECTOR) and 
            self.is_element_present(self.PASSWORD_SELECTOR)):
            return True
        
        return False
    
    # ==================== PASO 3: LOGIN ====================
    
    def perform_login(self, email, password):
        """
        Paso 3: Realizar login desde formulario en la página actual.
        
        Logs generados:
        1. 🔎 BUSCANDO ELEMENTO: [name="session_key"]
        2. ✓ ELEMENTO ENCONTRADO: [name="session_key"] - Campo de email
        3. 🧹 ACCIÓN → LIMPIAR: Campo de email
        4. ⌨️ ACCIÓN → ESCRIBIR: Campo de email → 'sergio...'
        5. 🔎 BUSCANDO ELEMENTO: [name="session_password"]
        6. ✓ ELEMENTO ENCONTRADO: [name="session_password"] - Campo de password
        7. 🧹 ACCIÓN → LIMPIAR: Campo de password
        8. ⌨️ ACCIÓN → ESCRIBIR: Campo de password → '●●●●●●●●'
        9. 🔎 BUSCANDO ELEMENTO: [data-id="sign-in-form__submit-btn"] - Botón de login (clickable)
        10. ✓ ELEMENTO ENCONTRADO: [data-id="sign-in-form__submit-btn"] - Botón de login (clickable)
        11. 👆 ACCIÓN → CLICK: Botón de login
        """
        # Llenar email
        email_success = self.safe_send_keys(
            self.EMAIL_SELECTOR, 
            email, 
            "Campo de email"
        )
        
        if not email_success:
            return False
        
        # Llenar password
        password_success = self.safe_send_keys(
            self.PASSWORD_SELECTOR, 
            password, 
            "Campo de password"
        )
        
        if not password_success:
            return False
        
        # Clic en botón de login
        login_success = self.safe_click(
            self.LOGIN_BUTTON_SELECTOR,
            "Botón de login"
        )
        
        return login_success
    
    # ==================== PASO 4: BÚSQUEDA DE TRABAJO ====================
    
    def search_job(self, job_title=None):
        """
        Paso 4: Realizar búsqueda de trabajo.
        
        Logs generados:
        1. BUSCANDO ELEMENTO: [placeholder="Title, skill or Company"] - Campo de búsqueda
        2. ELEMENTO ENCONTRADO: [placeholder="Title, skill or Company"] - Campo de búsqueda
        3. ELEMENTO ACCIONADO: Campo de búsqueda de trabajos - send_keys: Python Developer
        4. BUSCANDO ELEMENTO: .jobs-search-box__submit-button - Botón de búsqueda (clickable)
        5. ELEMENTO ENCONTRADO: .jobs-search-box__submit-button - Botón de búsqueda (clickable)
        6. ELEMENTO ACCIONADO: Botón de búsqueda - click
        7. PAGINA CARGO COMPLETAMENTE (después de búsqueda)
        """
        job_title = job_title or settings.JOB_SEARCH_QUERY
        
        # Buscar el campo de búsqueda
        search_input = self.safe_find_element(
            self.SEARCH_INPUT_SELECTOR,
            "Campo de búsqueda de trabajos"
        )
        
        if not search_input:
            return False
        
        try:
            # Limpiar y escribir la búsqueda
            search_input.clear()
            search_input.send_keys(job_title)
            logger.element_action("Campo de búsqueda de trabajos", f"send_keys: {job_title}")
            
            # presionar Enter
            search_input.send_keys(Keys.RETURN)
            logger.element_action("Campo de búsqueda de trabajos", "send_keys: ENTER")
            
            # Esperar a que los resultados carguen
            self.wait_for_dom_ready()
            return True
            
        except Exception as e:
            return False