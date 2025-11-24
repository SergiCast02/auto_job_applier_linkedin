from utils.web_driver import WebDriverManager
from core.navigation_manager import NavigationManager
from config.settings import settings
from utils.logger import logger

def main():
    driver_manager = WebDriverManager()
    
    try:
        logger.system("INICIANDO LINKEDIN JOBS - BÚSQUEDA AUTOMÁTICA")
        logger.debug(f"Configuración LOG_LEVEL: {settings.LOG_LEVEL}")
        logger.info(f"Búsqueda configurada: '{settings.JOB_SEARCH_QUERY}'")
        
        # Configurar driver
        driver = driver_manager.setup_driver()
        
        # Navegación y búsqueda
        nav_manager = NavigationManager(driver)
        
        if nav_manager.go_to_jobs_and_search():
            logger.success("MISIÓN CUMPLIDA: Búsqueda de trabajo completada")
            logger.info(f"URL final: {driver.current_url}")
        else:
            logger.error("No se pudo completar la búsqueda de trabajo")
        
    except Exception as e:
        logger.error(f"Error crítico: {e}")
    
    finally:
        if settings.CLOSE_BROWSER:
            driver_manager.teardown_driver()
        else:
            logger.info("Navegador mantenido abierto")
            input("Presiona Enter para cerrar...")
            driver_manager.teardown_driver()

if __name__ == "__main__":
    main()