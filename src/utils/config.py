"""
Configuration management for VT Scanner.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from .logger import get_logger

logger = get_logger(__name__)


class Config:
    """Application configuration."""
    
    def __init__(self):
        self.api_key: str = ""
        self.scan_interval: int = 3600
        self.auto_export: bool = False
        self.export_format: str = "json"
        self.log_level: str = "INFO"
        self.history_file: str = "scan_history.json"
        self.dark_mode: bool = True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "api_key": self.api_key,
            "scan_interval": self.scan_interval,
            "auto_export": self.auto_export,
            "export_format": self.export_format,
            "log_level": self.log_level,
            "history_file": self.history_file,
            "dark_mode": self.dark_mode
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create Config from dictionary."""
        config = cls()
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config


def setup_environment() -> None:
    """Setup environment variables from .env file."""
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv(env_file)
        logger.info("Loaded environment from .env file")
    else:
        logger.debug("No .env file found, using system environment")
        
        
def get_api_key() -> Optional[str]:
    """Get VirusTotal API key from environment."""
    api_key = os.getenv("VT_API_KEY")
    
    if not api_key:
        logger.warning("VT_API_KEY not found in environment")
        
    return api_key
    
    
def load_config(config_path: str = "config.yaml") -> Config:
    """Load configuration from YAML file."""
    config = Config()
    config_file = Path(config_path)
    
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    config = Config.from_dict(data)
            logger.info(f"Loaded configuration from {config_path}")
        except (yaml.YAMLError, IOError) as e:
            logger.error(f"Error loading config: {e}")
    else:
        logger.debug(f"No config file found at {config_path}, using defaults")
        
    return config
    
    
def save_config(config: Config, config_path: str = "config.yaml") -> None:
    """Save configuration to YAML file."""
    try:
        with open(config_path, "w") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False)
        logger.info(f"Saved configuration to {config_path}")
    except IOError as e:
        logger.error(f"Error saving config: {e}")
