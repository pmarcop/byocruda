import pytest
from pathlib import Path
from byocruda.core.config import Settings

def test_load_config():
    """Test loading configuration from TOML file."""
    config_path = Path("config/config.toml")
    settings = Settings.from_toml(config_path)
    
    assert settings.api.host == "127.0.0.1"
    assert settings.api.port == 8000
    assert settings.api.project_name == "BYOCRUDA"
    assert settings.database.url == "sqlite:///./byocruda.db"
    assert settings.security.algorithm == "HS256"
    assert settings.logging.level == "INFO"
    assert settings.logging.file_path == "logs/byocruda.log"
    assert settings.logging.rotation == "500 MB"
    assert settings.logging.retention == "10 days"

def test_invalid_config_path():
    """Test handling of invalid config file path."""
    with pytest.raises(FileNotFoundError):
        Settings.from_toml(Path("nonexistent/config.toml"))
