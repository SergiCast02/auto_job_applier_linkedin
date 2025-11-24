from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverManager:
    """
    Gestor de WebDriver completamente funcional.
    Configurado para cargar todos los recursos (imágenes, CSS, JS, etc.)
    """
    
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        """
        Configura el navegador Chrome con opciones optimizadas para LinkedIn.
        Carga completa de recursos: imágenes, CSS, JS, fuentes, etc.
        """
        chrome_options = Options()
        
        # ==================== CONFIGURACIÓN DE VENTANA ====================
        chrome_options.add_argument("--start-maximized")
        
        # ==================== CONFIGURACIÓN ANTI-DETECCIÓN ====================
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # ==================== CONFIGURACIÓN DE IDIOMA ====================
        chrome_options.add_argument("--lang=en-US")
        
        # ==================== CONFIGURACIÓN DE USER AGENT ====================
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        
        # ==================== CONFIGURACIÓN DE CARGA COMPLETA ====================
        # CRÍTICO: Habilitar TODAS las imágenes y recursos
        chrome_options.add_experimental_option('prefs', {
            # Idioma y región
            'intl.accept_languages': 'en-US,en',
            
            # CARGAR TODAS LAS IMÁGENES (foto de perfil, logos, etc.)
            'profile.managed_default_content_settings.images': 1,  # 1 = PERMITIR, 2 = BLOQUEAR
            'profile.default_content_setting_values.images': 1,
            
            # Habilitar JavaScript
            'profile.managed_default_content_settings.javascript': 1,
            
            # Habilitar CSS
            'profile.managed_default_content_settings.stylesheets': 1,
            
            # Habilitar cookies
            'profile.managed_default_content_settings.cookies': 1,
            
            # Habilitar plugins
            'profile.managed_default_content_settings.plugins': 1,
            
            # Habilitar notificaciones (opcional, puede deshabilitarse)
            'profile.default_content_setting_values.notifications': 2,  # 2 = BLOQUEAR
            
            # Deshabilitar popups molestos
            'profile.default_content_setting_values.popups': 2,
            
            # Configuración de descarga
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })
        
        # ==================== CONFIGURACIÓN DE RENDIMIENTO ====================
        # Estas opciones mejoran el rendimiento SIN bloquear recursos
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")  # Opcional, puede comentarse si causa problemas
        
        # ==================== CONFIGURACIÓN DE RED ====================
        # Mejorar la carga de recursos de red
        chrome_options.add_argument("--disable-web-security")  # SOLO para testing, no usar en producción
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # ==================== CREAR DRIVER ====================
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # ==================== SCRIPTS ANTI-DETECCIÓN ====================
        # Ocultar que estamos usando WebDriver
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        # Sobrescribir el objeto navigator para parecer más humano
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })
        
        # Agregar plugins comunes
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)
        
        # Agregar idiomas
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)
        
        # ==================== TIMEOUTS ====================
        # Timeout implícito más largo para permitir carga completa
        self.driver.implicitly_wait(5)
        
        # Timeout de página completo
        self.driver.set_page_load_timeout(30)
        
        # Timeout de script
        self.driver.set_script_timeout(30)
        
        return self.driver
    
    def teardown_driver(self):
        """
        Cierra el navegador.
        Operación silenciosa - no genera logs.
        """
        if self.driver:
            self.driver.quit()
    
    def wait_for_navigation(self, timeout=15):
        """
        Espera inteligente a que la navegación termine COMPLETAMENTE.
        Espera a que se carguen todos los recursos.
        """
        try:
            # Esperar a que el documento esté completo
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Esperar adicional para recursos asíncronos (imágenes, fuentes, etc.)
            import time
            time.sleep(1)
            
        except:
            pass
    
    def navigate_and_wait(self, url):
        """
        Navega y espera de forma inteligente a carga completa.
        Método interno - no genera logs.
        """
        self.driver.get(url)
        self.wait_for_navigation(15)