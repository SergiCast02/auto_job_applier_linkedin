from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from config.settings import settings
from utils.logger import logger

class JobsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Selectores como constantes
        self.EMAIL_SELECTOR = '[name="session_key"]'
        self.PASSWORD_SELECTOR = '[name="session_password"]'
        self.LOGIN_BUTTON_SELECTOR = '[data-id="sign-in-form__submit-btn"][type="submit"]'
        self.JOBS_INDICATOR = ".jobs-search-two-pane__wrapper"
        self.LOGIN_FORM_SELECTOR = 'form[data-id="sign-in-form"]'
    
    def navigate_to_jobs(self):
        logger.system("Navegando a LinkedIn Jobs...")
        return self.navigate_to("https://www.linkedin.com/jobs/")
    
    def is_jobs_page_loaded(self):
        """Verifica si jobs cargó correctamente (sin formulario de login)"""
        try:
            # Primero verificar que estamos en la URL correcta
            if "jobs" not in self.get_current_url().lower():
                logger.debug("No estamos en la URL de jobs")
                return False
            
            # Verificar si hay formulario de login visible
            if self.is_login_form_present():
                logger.warning("Jobs cargó pero muestra formulario de login")
                return False
            
            # Verificar elementos de jobs de forma segura
            jobs_element = self.safe_find_element(
                self.JOBS_INDICATOR, 
                "Indicador de página de Jobs"
            )
            
            if jobs_element:
                logger.success("Jobs cargado correctamente (sin login requerido)")
                return True
            else:
                logger.debug("Indicador de Jobs no encontrado")
                return False
            
        except Exception as e:
            logger.debug(f"Error verificando carga de Jobs: {e}")
            return False
    
    def is_login_form_present(self):
        """Detecta si el formulario de login está presente en la página de jobs"""
        # Verificar formulario de login
        if self.is_element_present(self.LOGIN_FORM_SELECTOR):
            logger.debug("Formulario de login detectado por selector .login__form")
            return True
        
        # Verificar campos de email/password
        if (self.is_element_present(self.EMAIL_SELECTOR) and 
            self.is_element_present(self.PASSWORD_SELECTOR)):
            logger.debug("Campos de login detectados en página de Jobs")
            return True
        
        return False
    
    def is_login_required(self):
        """Detección mejorada de requerimiento de login"""
        current_url = self.get_current_url().lower()
        
        # Si estamos en página de login específica
        if any(indicator in current_url for indicator in ["login", "signin", "authwall"]):
            logger.debug("Login requerido detectado por URL")
            return True
        
        # Si estamos en /jobs pero con formulario de login visible
        if "jobs" in current_url and self.is_login_form_present():
            logger.debug("Login requerido detectado por formulario en Jobs")
            return True
        
        logger.debug("No se requiere login aparentemente")
        return False
    
    def perform_login_from_jobs(self, email, password):
        """Realiza login directamente desde la página de jobs de forma segura"""
        logger.info("Realizando login desde página de Jobs...")
        
        # Buscar y llenar email de forma segura
        email_success = self.safe_send_keys(
            self.EMAIL_SELECTOR, 
            email, 
            "Campo de email"
        )
        
        if not email_success:
            logger.error("No se pudo encontrar el campo de email")
            return False
        
        # Buscar y llenar password de forma segura
        password_success = self.safe_send_keys(
            self.PASSWORD_SELECTOR, 
            password, 
            "Campo de password"
        )
        
        if not password_success:
            logger.error("No se pudo encontrar el campo de password")
            return False
        
        # Hacer clic en el botón de login de forma segura
        login_success = self.safe_click(
            self.LOGIN_BUTTON_SELECTOR,
            "Botón de login"
        )
        
        if login_success:
            logger.success("Login desde Jobs enviado")
            return True
        else:
            logger.error("No se pudo hacer clic en el botón de login")
            return False
    
    def wait_for_jobs_after_login(self, timeout=10):
        """Espera a que jobs cargue después del login"""
        import time
        start_time = time.time()
        
        logger.debug("Esperando a que Jobs cargue después del login...")
        
        while time.time() - start_time < timeout:
            # Verificar si jobs cargó correctamente
            if self.is_jobs_page_loaded():
                logger.success("Jobs cargado después del login")
                return True
            
            # Si todavía hay formulario de login, el login falló
            if self.is_login_form_present():
                logger.warning("Formulario de login aún presente después del intento")
                return False
            
            # Verificar si hay errores de login
            if self._check_login_errors():
                logger.error("Error de login detectado")
                return False
            
            time.sleep(0.5)
        
        logger.warning("Timeout esperando jobs después del login")
        return False
    
    def _check_login_errors(self):
        """Verifica si hay mensajes de error de login"""
        error_selectors = [
            ".error-for-username",
            ".error-for-password", 
            ".alert-error",
            "[data-test-id='login-error']"
        ]
        
        for selector in error_selectors:
            if self.is_element_present(selector):
                error_element = self.safe_find_element(selector, "Mensaje de error")
                if error_element:
                    error_text = error_element.text.strip()
                    if error_text:
                        logger.error(f"Error de login: {error_text}")
                        return True
        return False