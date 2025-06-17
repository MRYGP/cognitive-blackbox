"""
Cognitive Black Box - Application Configuration Management
Centralized configuration with environment variable support
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class APIConfig:
    """AI API configuration settings"""
    gemini_api_key: str
    anthropic_api_key: str
    gemini_model: str = "gemini-2.0-flash-exp"
    claude_model: str = "claude-3-5-sonnet-20241022"
    default_temperature: float = 0.7
    max_tokens: int = 4000
    request_timeout: int = 30

@dataclass
class SessionConfig:
    """Session management configuration"""
    timeout_minutes: int = 30
    max_api_calls_per_session: int = 100
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600
    secret_key: str = "default_secret_key_change_in_production"

@dataclass
class AppConfig:
    """Main application configuration"""
    app_name: str = "Cognitive Black Box"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug_mode: bool = True
    show_debug_ui: bool = True
    enable_performance_log: bool = True

@dataclass
class FeatureFlags:
    """Feature flags for experimental features"""
    enable_experimental_features: bool = False
    enable_ab_testing: bool = False
    enable_analytics: bool = False
    mock_api_responses: bool = False
    test_mode: bool = False

@dataclass
class SecurityConfig:
    """Security related configuration"""
    enable_rate_limiting: bool = True
    requests_per_minute: int = 60
    require_https: bool = False
    cors_enabled: bool = True

class ConfigManager:
    """
    Centralized configuration manager
    Loads settings from environment variables with fallback defaults
    """
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        self._api_config = None
        self._session_config = None
        self._app_config = None
        self._feature_flags = None
        self._security_config = None
        
        self._load_configs()
    
    def _load_configs(self) -> None:
        """Load all configuration sections"""
        self._api_config = APIConfig(
            gemini_api_key=self._get_env_var("GEMINI_API_KEY", required=True),
            anthropic_api_key=self._get_env_var("ANTHROPIC_API_KEY", required=True),
            gemini_model=self._get_env_var("GEMINI_MODEL", "gemini-2.0-flash-exp"),
            claude_model=self._get_env_var("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
            default_temperature=float(self._get_env_var("DEFAULT_TEMPERATURE", "0.7")),
            max_tokens=int(self._get_env_var("MAX_TOKENS", "4000")),
            request_timeout=int(self._get_env_var("REQUEST_TIMEOUT", "30"))
        )
        
        self._session_config = SessionConfig(
            timeout_minutes=int(self._get_env_var("SESSION_TIMEOUT_MINUTES", "30")),
            max_api_calls_per_session=int(self._get_env_var("MAX_API_CALLS_PER_SESSION", "100")),
            enable_cache=self._get_bool_env("ENABLE_CACHE", True),
            cache_ttl_seconds=int(self._get_env_var("CACHE_TTL_SECONDS", "3600")),
            secret_key=self._get_env_var("SECRET_KEY", "default_secret_key_change_in_production")
        )
        
        self._app_config = AppConfig(
            environment=self._get_env_var("APP_ENV", "development"),
            debug_mode=self._get_bool_env("DEBUG_MODE", True),
            show_debug_ui=self._get_bool_env("SHOW_DEBUG_UI", True),
            enable_performance_log=self._get_bool_env("ENABLE_PERFORMANCE_LOG", True)
        )
        
        self._feature_flags = FeatureFlags(
            enable_experimental_features=self._get_bool_env("ENABLE_EXPERIMENTAL_FEATURES", False),
            enable_ab_testing=self._get_bool_env("ENABLE_AB_TESTING", False),
            enable_analytics=self._get_bool_env("ENABLE_ANALYTICS", False),
            mock_api_responses=self._get_bool_env("MOCK_API_RESPONSES", False),
            test_mode=self._get_bool_env("TEST_MODE", False)
        )
        
        self._security_config = SecurityConfig(
            enable_rate_limiting=self._get_bool_env("ENABLE_RATE_LIMITING", True),
            requests_per_minute=int(self._get_env_var("REQUESTS_PER_MINUTE", "60")),
            require_https=self._get_bool_env("REQUIRE_HTTPS", False),
            cors_enabled=self._get_bool_env("CORS_ENABLED", True)
        )
    
    def _get_env_var(self, key: str, default: Optional[str] = None, required: bool = False) -> str:
        """
        Get environment variable with optional default and required check
        
        Args:
            key: Environment variable key
            default: Default value if not found
            required: Whether the variable is required
        
        Returns:
            str: Environment variable value
        
        Raises:
            ValueError: If required variable is not found
        """
        value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        
        return value or ""
    
    def _get_bool_env(self, key: str, default: bool = False) -> bool:
        """
        Get boolean environment variable
        
        Args:
            key: Environment variable key
            default: Default boolean value
        
        Returns:
            bool: Boolean value
        """
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")
    
    @property
    def api(self) -> APIConfig:
        """Get API configuration"""
        return self._api_config
    
    @property
    def session(self) -> SessionConfig:
        """Get session configuration"""
        return self._session_config
    
    @property
    def app(self) -> AppConfig:
        """Get app configuration"""
        return self._app_config
    
    @property
    def features(self) -> FeatureFlags:
        """Get feature flags"""
        return self._feature_flags
    
    @property
    def security(self) -> SecurityConfig:
        """Get security configuration"""
        return self._security_config
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self._app_config.environment == "development"
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self._app_config.environment == "production"
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """
        Validate that required API keys are present
        
        Returns:
            Dict[str, bool]: Validation results for each API
        """
        return {
            "gemini": bool(self._api_config.gemini_api_key and self._api_config.gemini_api_key != "your_gemini_api_key_here"),
            "anthropic": bool(self._api_config.anthropic_api_key and self._api_config.anthropic_api_key != "your_anthropic_api_key_here")
        }
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """
        Get configuration for Streamlit app setup
        
        Returns:
            Dict[str, Any]: Streamlit configuration
        """
        return {
            "page_title": self._app_config.app_name,
            "page_icon": "🧠",
            "layout": "wide",
            "initial_sidebar_state": "collapsed"
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary (for debugging)
        Note: API keys are masked for security
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            "api": {
                "gemini_api_key": "***" if self._api_config.gemini_api_key else "Not Set",
                "anthropic_api_key": "***" if self._api_config.anthropic_api_key else "Not Set",
                "gemini_model": self._api_config.gemini_model,
                "claude_model": self._api_config.claude_model,
                "default_temperature": self._api_config.default_temperature,
                "max_tokens": self._api_config.max_tokens,
                "request_timeout": self._api_config.request_timeout
            },
            "session": {
                "timeout_minutes": self._session_config.timeout_minutes,
                "max_api_calls_per_session": self._session_config.max_api_calls_per_session,
                "enable_cache": self._session_config.enable_cache,
                "cache_ttl_seconds": self._session_config.cache_ttl_seconds,
                "secret_key": "***" if self._session_config.secret_key else "Not Set"
            },
            "app": {
                "app_name": self._app_config.app_name,
                "app_version": self._app_config.app_version,
                "environment": self._app_config.environment,
                "debug_mode": self._app_config.debug_mode,
                "show_debug_ui": self._app_config.show_debug_ui,
                "enable_performance_log": self._app_config.enable_performance_log
            },
            "features": {
                "enable_experimental_features": self._feature_flags.enable_experimental_features,
                "enable_ab_testing": self._feature_flags.enable_ab_testing,
                "enable_analytics": self._feature_flags.enable_analytics,
                "mock_api_responses": self._feature_flags.mock_api_responses,
                "test_mode": self._feature_flags.test_mode
            },
            "security": {
                "enable_rate_limiting": self._security_config.enable_rate_limiting,
                "requests_per_minute": self._security_config.requests_per_minute,
                "require_https": self._security_config.require_https,
                "cors_enabled": self._security_config.cors_enabled
            }
        }

# Global configuration instance
config = ConfigManager()

# Convenience functions for common config access
def get_api_config() -> APIConfig:
    """Get API configuration"""
    return config.api

def get_session_config() -> SessionConfig:
    """Get session configuration"""
    return config.session

def get_app_config() -> AppConfig:
    """Get app configuration"""
    return config.app

def get_feature_flags() -> FeatureFlags:
    """Get feature flags"""
    return config.features

def is_debug_mode() -> bool:
    """Check if debug mode is enabled"""
    return config.app.debug_mode

def validate_setup() -> Dict[str, bool]:
    """
    Validate that the application is properly configured
    
    Returns:
        Dict[str, bool]: Validation results
    """
    api_validation = config.validate_api_keys()
    
    return {
        "api_keys_valid": all(api_validation.values()),
        "gemini_available": api_validation["gemini"],
        "anthropic_available": api_validation["anthropic"],
        "config_loaded": True
    }
