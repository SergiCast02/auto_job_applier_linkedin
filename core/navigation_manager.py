from pages.jobs_page import JobsPage
from core.session_manager import SessionManager
from config.settings import settings
from utils.logger import logger

class NavigationManager:
    """
    Gestor de navegación con lógica simplificada y logs bonitos:
    
    1. Cargar https://www.linkedin.com/jobs/
    2. Si NO hay formulario de login → Buscar empleo
    3. Si SÍ hay formulario de login → Loguearse y volver a /jobs/
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.session_manager = SessionManager()
        self.jobs_page = JobsPage(driver)
    
    def go_to_jobs_and_search(self):
        """
        Flujo simplificado con logs diferenciados:
        1. Ir a https://www.linkedin.com/jobs/
        2. Verificar si hay formulario de login
        3. Si NO hay formulario → Buscar
        4. Si SÍ hay formulario → Login y volver a intentar
        """
        
        logger.section("🚀 INICIANDO PROCESO DE BÚSQUEDA EN LINKEDIN JOBS")
        logger.info(f"Búsqueda configurada: '{settings.JOB_SEARCH_QUERY}'")
        logger.separator()
        
        # PASO 1: Cargar cookies y navegar
        logger.section("📂 PASO 1: CARGANDO SESIÓN Y NAVEGANDO")
        self._load_cookies_if_exist()
        self.jobs_page.navigate_to_jobs()
        logger.separator()
        
        # PASO 2: Verificar si hay formulario de login
        logger.section("🔍 PASO 2: VERIFICANDO ESTADO DE AUTENTICACIÓN")
        has_login_form = self.jobs_page.is_login_form_present()
        
        if not has_login_form:
            # NO hay formulario → Hacer búsqueda directamente
            logger.success("✓ Sesión activa - No se requiere login")
            logger.separator()
            
            logger.section("🔎 PASO 3: REALIZANDO BÚSQUEDA DE EMPLEO")
            success = self.jobs_page.search_job()
            logger.separator()
            
            if success:
                logger.success("🎉 BÚSQUEDA COMPLETADA EXITOSAMENTE")
            else:
                logger.error("❌ ERROR: No se pudo completar la búsqueda")
            
            return success
        
        # SÍ hay formulario → Hacer login
        logger.info("⚠️  Se requiere autenticación")
        logger.separator()
        
        # PASO 3: Realizar login
        logger.section("🔐 PASO 3: INICIANDO SESIÓN")
        if not self.jobs_page.perform_login(settings.EMAIL, settings.PASSWORD):
            logger.error("❌ ERROR: Fallo al enviar credenciales")
            return False
        
        # Esperar a que se complete el login
        if not self._wait_for_login_redirect():
            logger.error("❌ ERROR: Login no completado o credenciales incorrectas")
            return False
        
        logger.success("✓ Login exitoso - Sesión establecida")
        logger.separator()
        
        # PASO 4: Volver a /jobs/ después del login
        logger.section("🔄 PASO 4: VOLVIENDO A LINKEDIN JOBS")
        self.jobs_page.navigate_to_jobs()
        logger.separator()
        
        # PASO 5: Verificar que ya no haya formulario
        logger.section("✅ PASO 5: VERIFICANDO AUTENTICACIÓN")
        if self.jobs_page.is_login_form_present():
            # Login falló, todavía pide credenciales
            logger.error("❌ ERROR: Autenticación fallida - Formulario aún presente")
            return False
        
        logger.success("✓ Autenticación verificada")
        logger.separator()
        
        # PASO 6: Realizar búsqueda
        logger.section("🔎 PASO 6: REALIZANDO BÚSQUEDA DE EMPLEO")
        success = self.jobs_page.search_job()
        logger.separator()
        
        if success:
            logger.success("🎉 BÚSQUEDA COMPLETADA EXITOSAMENTE")
        else:
            logger.error("❌ ERROR: No se pudo completar la búsqueda")
        
        return success
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _load_cookies_if_exist(self):
        """Carga cookies si existen (silencioso)"""
        if self.session_manager.cookies_exist():
            logger.info("📝 Cargando cookies de sesión anterior...")
            return self.session_manager.load_cookies(self.driver)
        else:
            logger.info("📝 No se encontraron cookies - Primera ejecución")
        return False
    
    def _wait_for_login_redirect(self):
        """
        Espera a que se complete el login y redirija.
        Verifica que ya no estemos en página de login.
        """
        import time
        start_time = time.time()
        
        logger.info("⏳ Esperando redirección después del login...")
        
        while time.time() - start_time < 10:
            current_url = self.driver.current_url.lower()
            
            # Si ya no estamos en página de login, éxito
            if "login" not in current_url and "signin" not in current_url:
                # Guardar cookies para próxima vez
                logger.info("💾 Guardando cookies de sesión...")
                self.session_manager.save_cookies(self.driver)
                return True
            
            # Si después de 3 segundos todavía hay formulario, falló
            if time.time() - start_time > 3 and self.jobs_page.is_login_form_present():
                return False
            
            time.sleep(0.5)
        
        return False