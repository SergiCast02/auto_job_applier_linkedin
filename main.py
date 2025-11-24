from utils.web_driver import WebDriverManager
from core.navigation_manager import NavigationManager
from config.settings import settings
from utils.logger import logger

def main():
    """
    Script principal - Flujo de ejecución con logs bonitos y diferenciados.
    
    Los logs ahora incluyen:
    - 📄 PAGINA CARGO COMPLETAMENTE
    - 🔗 URL
    - 🔎 BUSCANDO ELEMENTO
    - ✓ ELEMENTO ENCONTRADO
    - 👆 ACCIÓN → CLICK
    - ⌨️ ACCIÓN → ESCRIBIR
    - 🧹 ACCIÓN → LIMPIAR
    - 📤 ACCIÓN → SUBMIT
    - ✅ Mensajes de éxito
    - ❌ Mensajes de error
    - ℹ️ Información general
    """
    driver_manager = WebDriverManager()
    
    try:
        # Banner inicial
        print("\n" + "=" * 80)
        print("🚀 LINKEDIN JOBS - AUTOMATIZACIÓN DE BÚSQUEDA DE EMPLEO")
        print("=" * 80 + "\n")
        
        # Configurar driver (silencioso)
        driver = driver_manager.setup_driver()
        
        # Navegación y búsqueda (con logs detallados)
        nav_manager = NavigationManager(driver)
        success = nav_manager.go_to_jobs_and_search()
        
        # Resumen final
        print("\n" + "=" * 80)
        if success:
            logger.success("🎉 PROCESO COMPLETADO EXITOSAMENTE")
            logger.info(f"📍 URL final: {driver.current_url}")
        else:
            logger.error("❌ PROCESO COMPLETADO CON ERRORES")
            logger.info(f"📍 URL actual: {driver.current_url}")
        print("=" * 80 + "\n")
        
    except KeyboardInterrupt:
        logger.error("\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico: {str(e)}")
    
    finally:
        if settings.CLOSE_BROWSER:
            logger.info("🔚 Cerrando navegador...")
            driver_manager.teardown_driver()
        else:
            logger.info("🔄 Navegador mantenido abierto para inspección")
            input("\n⏸️  Presiona Enter para cerrar el navegador...")
            driver_manager.teardown_driver()

if __name__ == "__main__":
    main()