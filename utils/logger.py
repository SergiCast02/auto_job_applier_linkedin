import os
import sys
from datetime import datetime
from colorama import init, Fore, Back, Style
from config.settings import settings

# Inicializar colorama para colores en Windows/Linux/Mac
init()

class Logger:
    """
    Logger modularizado con logs bonitos y diferenciados:
    1. PAGINA CARGO COMPLETAMENTE (DOMContentLoaded)
    2. URL de la pagina
    3. BUSCANDO ELEMENTO
    4. ELEMENTO ENCONTRADO
    5. ELEMENTO ACCIONADO (con tipos diferenciados)
    """
    
    def __init__(self):
        self.levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3
        }
        self.current_level = self.levels.get(settings.LOG_LEVEL, 1)
        self.colors = {
            'PAGE': Fore.GREEN,
            'URL': Fore.CYAN,
            'SEARCHING': Fore.LIGHTYELLOW_EX,
            'FOUND': Fore.YELLOW,
            'ACTION_CLICK': Fore.MAGENTA,
            'ACTION_SEND': Fore.LIGHTBLUE_EX,
            'ACTION_OTHER': Fore.LIGHTMAGENTA_EX,
            'SUCCESS': Fore.LIGHTGREEN_EX,
            'ERROR': Fore.RED,
            'TIMESTAMP': Fore.WHITE,
            'RESET': Style.RESET_ALL
        }
    
    def _get_timestamp(self):
        """Genera timestamp según configuración"""
        now = datetime.now()
        
        time_format = "%I:%M %p"  # 06:00 PM
        day_format = ""
        date_format = ""
        
        if settings.LOG_SHOW_TIME:
            time_format = "%I:%M %p"
        
        if settings.LOG_SHOW_DAY:
            day_format = " - %A"
        
        if settings.LOG_SHOW_DATE:
            date_format = " - %d/%m/%Y"
        
        format_str = time_format + day_format + date_format
        return now.strftime(format_str)
    
    def _should_log(self, level):
        """Verifica si el nivel debe ser mostrado"""
        return self.levels[level] >= self.current_level
    
    def _print_log(self, emoji, color, message):
        """Método interno unificado para imprimir logs"""
        if not self._should_log('INFO'):
            return
        
        timestamp = self._get_timestamp()
        log_message = f"{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} {emoji} {color}{message}{self.colors['RESET']}"
        print(log_message)
    
    # ==================== MÉTODOS PRINCIPALES ====================
    
    def page_loaded(self, url):
        """✅ PAGINA CARGO COMPLETAMENTE (DOMContentLoaded)"""
        self._print_log('📄', self.colors['PAGE'], f"PAGINA CARGO COMPLETAMENTE (DOMContentLoaded)")
    
    def current_url(self, url):
        """✅ URL de la pagina"""
        self._print_log('🔗', self.colors['URL'], f"URL: {url}")
    
    def searching_element(self, selector, description=""):
        """✅ BUSCANDO ELEMENTO"""
        desc = f" - {description}" if description else ""
        self._print_log('🔎', self.colors['SEARCHING'], f"BUSCANDO ELEMENTO: {selector}{desc}")
    
    def element_found(self, selector, description=""):
        """✅ ELEMENTO ENCONTRADO"""
        desc = f" - {description}" if description else ""
        self._print_log('✓', self.colors['FOUND'], f"ELEMENTO ENCONTRADO: {selector}{desc}")
    
    # ==================== ACCIONES DIFERENCIADAS ====================
    
    def action_click(self, element_name):
        """✅ ACCIÓN: Click en elemento"""
        self._print_log('👆', self.colors['ACTION_CLICK'], f"ACCIÓN → CLICK: {element_name}")
    
    def action_send_keys(self, element_name, text):
        """✅ ACCIÓN: Escribir texto en elemento"""
        # Ocultar passwords
        if "password" in element_name.lower() or "contraseña" in element_name.lower():
            display_text = "●" * len(text)
        else:
            # Mostrar primeros 30 caracteres del texto
            display_text = text[:30] + "..." if len(text) > 30 else text
        
        self._print_log('⌨️', self.colors['ACTION_SEND'], f"ACCIÓN → ESCRIBIR: {element_name} → '{display_text}'")
    
    def action_clear(self, element_name):
        """✅ ACCIÓN: Limpiar campo"""
        self._print_log('🧹', self.colors['ACTION_OTHER'], f"ACCIÓN → LIMPIAR: {element_name}")
    
    def action_submit(self, element_name):
        """✅ ACCIÓN: Submit/Enter en formulario"""
        self._print_log('📤', self.colors['ACTION_OTHER'], f"ACCIÓN → SUBMIT: {element_name}")
    
    # ==================== LOGS DE ESTADO ====================
    
    def success(self, message):
        """✅ Operación exitosa"""
        if self._should_log('INFO'):
            timestamp = self._get_timestamp()
            print(f"{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} ✅ {self.colors['SUCCESS']}{message}{self.colors['RESET']}")
    
    def error(self, message):
        """❌ Error en operación"""
        if self._should_log('INFO'):
            timestamp = self._get_timestamp()
            print(f"{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} ❌ {self.colors['ERROR']}{message}{self.colors['RESET']}")
    
    def info(self, message):
        """ℹ️ Información general"""
        if self._should_log('INFO'):
            timestamp = self._get_timestamp()
            print(f"{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} ℹ️  {Fore.LIGHTCYAN_EX}{message}{self.colors['RESET']}")
    
    def separator(self):
        """Separador visual"""
        if self._should_log('INFO'):
            print(f"{Fore.LIGHTBLACK_EX}{'─' * 80}{self.colors['RESET']}")
    
    def section(self, title):
        """Título de sección"""
        if self._should_log('INFO'):
            timestamp = self._get_timestamp()
            print(f"\n{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} {Back.BLUE}{Fore.WHITE} {title} {self.colors['RESET']}")
    
    # ==================== MÉTODOS DEPRECADOS ====================
    
    def debug(self, message):
        pass  # Silenciado
    
    def warning(self, message):
        pass  # Silenciado
    
    def system(self, message):
        pass  # Silenciado
    
    def element_action(self, element_name, action_name):
        """Método deprecado - usar action_click, action_send_keys, etc."""
        pass  # Redirigir a métodos específicos

# Instancia global del logger
logger = Logger()