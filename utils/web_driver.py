from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from .logger import logger

class WebDriverManager:
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        """Configura driver rápido sin esperas innecesarias"""
        logger.system("Configurando navegador...")
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--lang=en")
        
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': 'en,en_US',
            'profile.managed_default_content_settings.images': 2
        })
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver.implicitly_wait(2)
        
        logger.success("Navegador configurado")
        return self.driver
    
    def teardown_driver(self):
        if self.driver:
            self.driver.quit()
            logger.info("Navegador cerrado")
    
    def wait_for_navigation(self, timeout=10):
        """Espera inteligente a que la navegación termine"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except:
            pass
    
    def navigate_and_wait(self, url):
        """Navega y espera de forma inteligente"""
        self.driver.get(url)
        self.wait_for_navigation(5)