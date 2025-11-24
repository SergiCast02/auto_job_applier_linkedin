from pages.jobs_page import JobsPage
from core.session_manager import SessionManager
from config.settings import settings
from utils.logger import logger

class NavigationManager:
    def __init__(self, driver):
        self.driver = driver
        self.session_manager = SessionManager()
        self.jobs_page = JobsPage(driver)
    
    def go_to_jobs_directly(self):
        """Flujo mejorado que maneja login en página de jobs de forma segura"""
        logger.system("Iniciando acceso directo a Jobs...")
        
        # 1. Cargar cookies si existen
        cookies_loaded = False
        if self.session_manager.cookies_exist():
            logger.debug("Cookies encontradas, cargando...")
            cookies_loaded = self.session_manager.load_cookies(self.driver)
        
        # 2. Ir directamente a jobs
        self.jobs_page.navigate_to_jobs()
        
        # 3. Verificar estado de la página de forma segura
        if self.jobs_page.is_jobs_page_loaded():
            logger.success("Acceso directo a Jobs exitoso!")
            return True
        
        # 4. Si requiere login, determinar el tipo
        if self.jobs_page.is_login_required():
            logger.warning("Login requerido detectado")
            
            # Eliminar cookies si estaban presentes pero expiraron
            if cookies_loaded:
                logger.debug("Cookies expiradas, eliminando...")
                self.session_manager.delete_cookies()
            
            # Intentar login
            if self._handle_login():
                # Verificar que jobs cargó después del login
                if self.jobs_page.wait_for_jobs_after_login():
                    logger.success("Login exitoso y Jobs cargado!")
                    return True
                else:
                    logger.error("Login aparentemente exitoso pero Jobs no cargó")
                    return False
            else:
                logger.error("Login falló")
                return False
        
        # 5. Si llegamos aquí, no pudimos determinar el estado
        logger.warning("No se pudo determinar el estado de autenticación")
        logger.info(f"URL actual: {self.driver.current_url}")
        
        # Intentar una verificación final
        if "jobs" in self.driver.current_url.lower():
            logger.info("Estamos en Jobs pero no se pudo verificar el estado, continuando...")
            return True
        else:
            logger.error("No estamos en la página de Jobs")
            return False
    
    def _handle_login(self):
        """Maneja el login según el tipo de página"""
        current_url = self.driver.current_url.lower()
        
        # Si estamos en página de login específica
        if any(indicator in current_url for indicator in ["login", "signin", "authwall"]):
            logger.info("Redirigiendo a página de login específica...")
            return self._quick_login_standard()
        
        # Si estamos en /jobs con formulario de login
        elif "jobs" in current_url and self.jobs_page.is_login_form_present():
            logger.info("Realizando login desde página de Jobs...")
            return self._quick_login_from_jobs()
        
        else:
            logger.error("Tipo de login no reconocido")
            return False
    
    def _quick_login_standard(self):
        """Login desde página de login estándar"""
        self.jobs_page.navigate_to("https://www.linkedin.com/login")
        
        if self.jobs_page.perform_login_from_jobs(settings.EMAIL, settings.PASSWORD):
            return self._wait_for_login_redirect()
        return False
    
    def _quick_login_from_jobs(self):
        """Login directamente desde la página de jobs"""
        if self.jobs_page.perform_login_from_jobs(settings.EMAIL, settings.PASSWORD):
            return self._wait_for_login_redirect()
        return False
    
    def _wait_for_login_redirect(self):
        """Espera inteligente a la redirección después del login"""
        import time
        start_time = time.time()
        
        logger.debug("Esperando redirección después del login...")
        
        while time.time() - start_time < 8:
            current_url = self.driver.current_url.lower()
            
            # Si ya no estamos en página de login
            if "login" not in current_url and "signin" not in current_url:
                self.session_manager.save_cookies(self.driver)
                logger.debug("Redirección después del login detectada")
                return True
            
            # Si todavía hay formulario de login después de un tiempo, posible fallo
            if time.time() - start_time > 3 and self.jobs_page.is_login_form_present():
                logger.warning("Formulario de login aún presente después de 3 segundos")
                return False
            
            time.sleep(0.3)
        
        logger.warning("Timeout esperando redirección después del login")
        return False