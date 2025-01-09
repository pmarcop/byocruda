from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings
import tomli

class APISettings(BaseModel):
    host: str
    port: int
    debug: bool
    prefix: str
    project_name: str
    description: str
    version: str

class DatabaseSettings(BaseModel):
    url: str
    echo: bool

class SecuritySettingsDatabase(BaseModel):
    secret_key_env_variable: str
    crypt_algorithm: str

class SecuritySettingsApi(BaseModel):
    signing_algorithm: str
    access_token_expire_minutes: int

class SecuritySettingsLdap(BaseModel):
    ldap_uri: str
    ldap_bind_user: str
    ldap_base: str
    ldap_filter: str

class SecuritySettings(BaseModel):
    database_enable: bool
    ldap_enable: bool
    api_enable: bool
    https_enable: bool
    database: SecuritySettingsDatabase
    ldap: SecuritySettingsLdap
    api: SecuritySettingsApi



class LoggingSettings(BaseModel):
    level: str
    format: str
    file_path: str
    rotation: str
    retention: str

class Settings(BaseSettings):
    api: APISettings
    database: DatabaseSettings
    security: SecuritySettings
    logging: LoggingSettings

    @classmethod
    def from_toml(cls, config_path: Path) -> "Settings":
        """Load settings from a TOML file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, "rb") as f:
            config_dict = tomli.load(f)
        
        return cls.model_validate(config_dict)

def load_config() -> Settings:
    """Load configuration from the default location."""
    config_path = Path("config/config.toml")
    try:
        return Settings.from_toml(config_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration: {str(e)}")

# Create a global settings instance
settings = load_config()
