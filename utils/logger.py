import os
import sys
from datetime import datetime
from colorama import init, Fore, Back, Style
from config.settings import settings

# Inicializar colorama para colores en Windows/Linux/Mac
init()

class Logger:
    def __init__(self):
        self.levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3
        }
        self.current_level = self.levels.get(settings.LOG_LEVEL, 1)
        self.colors = {
            'DEBUG': Fore.CYAN,
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
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
    
    def _log(self, level, message, emoji=""):
        """Método interno para logging"""
        if not self._should_log(level):
            return
        
        timestamp = self._get_timestamp()
        color = self.colors[level]
        
        # Formato: [06:00 PM] 🔐 LEVEL: mensaje
        log_message = f"{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} {emoji} {color}{level}:{self.colors['RESET']} {message}"
        print(log_message)
    
    def debug(self, message):
        self._log('DEBUG', message, '🔍')
    
    def info(self, message):
        self._log('INFO', message, 'ℹ️ ')
    
    def warning(self, message):
        self._log('WARNING', message, '⚠️')
    
    def error(self, message):
        self._log('ERROR', message, '❌')
    
    def success(self, message):
        """Log personalizado para éxitos"""
        if self._should_log('INFO'):
            timestamp = self._get_timestamp()
            print(f"{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} ✅ {Fore.GREEN}SUCCESS:{self.colors['RESET']} {message}")
    
    def system(self, message):
        """Log personalizado para mensajes del sistema"""
        if self._should_log('INFO'):
            timestamp = self._get_timestamp()
            print(f"{self.colors['TIMESTAMP']}[{timestamp}]{self.colors['RESET']} 🚀 {Fore.BLUE}SYSTEM:{self.colors['RESET']} {message}")

# Instancia global del logger
logger = Logger()