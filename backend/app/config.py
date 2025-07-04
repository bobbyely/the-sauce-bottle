"""Configuration settings for the application."""
# Re-export from core.config for backward compatibility
from backend.app.core.config import Settings, settings, get_settings

__all__ = ["Settings", "settings", "get_settings"]
