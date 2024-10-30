from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BYOCRUDA"
    
    # These will be populated from environment variables or config file later
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    
    class Config:
        case_sensitive = True

settings = Settings()
