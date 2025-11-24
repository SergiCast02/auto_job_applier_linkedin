import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # URLs
    JOBS_URL = "https://www.linkedin.com/jobs/"
    LOGIN_URL = "https://www.linkedin.com/login"
    COOKIES_FILE = "cookies/linkedin_cookies.pkl"
    CLOSE_BROWSER = os.getenv("CLOSE_BROWSER", "True").lower() == "true"
    EMAIL = os.getenv("LINKEDIN_EMAIL")
    PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    # Nueva configuración de búsqueda de trabajo
    JOB_SEARCH_QUERY = os.getenv("JOB_SEARCH_QUERY", "Python Developer")
    
    # Logger settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
    LOG_SHOW_TIME = os.getenv("LOG_SHOW_TIME", "True").lower() == "true"
    LOG_SHOW_DAY = os.getenv("LOG_SHOW_DAY", "False").lower() == "true"
    LOG_SHOW_DATE = os.getenv("LOG_SHOW_DATE", "False").lower() == "true"

settings = Settings()