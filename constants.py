"""
Cognitive Black Box - Project Constants
All constant values used throughout the application
"""

from enum import Enum
from typing import Dict, List, Any

# =============================================================================
# APPLICATION CONSTANTS
# =============================================================================

APP_NAME = "Cognitive Black Box"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "18-minute cognitive upgrade experience"
APP_AUTHOR = "Cognitive Black Box Team"

# Experience timing
TOTAL_EXPERIENCE_MINUTES = 18
TOTAL_STEPS = 4
STEP_NAMES = ["introduction", "reality_check", "framework", "tools"]

# =============================================================================
# ROLE SYSTEM CONSTANTS
# =============================================================================

class RoleType(Enum):
    """AI role types for the experience"""
    HOST = "host"
    INVESTOR = "investor" 
    MENTOR = "mentor"
    ASSISTANT = "assistant"

# Role configuration
ROLE_CONFIG = {
    RoleType.HOST: {
        "name": "Host",
        "description": "Professional guidance and user onboarding",
        "color_theme": "blue",
        "step": 1,
        "emotion_target": "trust_building",
        "interaction_style": "authoritative_friendly"
    },
    RoleType.INVESTOR: {
        "name": "Investor",
        "description": "Reality disruption and cognitive shock",
        "color_theme": "red",
        "step": 2,
        "emotion_target": "cognitive_dissonance",
        "interaction_style": "direct_challenging"
    },
    RoleType.MENTOR: {
        "name": "Mentor",
        "description": "Framework construction and insight",
        "color_theme": "green",
        "step": 3,
        "emotion_target": "enlightenment",
        "interaction_style": "wise_explanatory"
    },
    RoleType.ASSISTANT: {
        "name": "Assistant",
        "description": "Tool creation and capability building",
        "color_theme": "cyan",
        "step": 4,
        "emotion_target": "empowerment",
        "interaction_style": "practical_supportive"
    }
}

# =============================================================================
# CASE STUDY CONSTANTS
# =============================================================================

class CaseType(Enum):
    """Available case studies"""
    MADOFF = "madoff"
    LTCM = "ltcm"
    LEHMAN = "lehman"

# Cognitive biases mapped to cases
COGNITIVE_BIASES = {
    CaseType.MADOFF: {
        "primary_bias": "halo_effect",
        "bias_category": "social_proof",
        "description": "The fatal halo of authority and reputation"
    },
    CaseType.LTCM: {
        "primary_bias": "overconfidence",
        "bias_category": "self_assessment",
        "description": "Nobel Prize hubris and model worship"
    },
    CaseType.LEHMAN: {
        "primary_bias": "confirmation_bias",
        "bias_category": "information_processing",
        "description": "The unshakeable belief in perpetual growth"
    }
}

# Case financial impact data
CASE_FINANCIAL_IMPACT = {
    CaseType.MADOFF: {
        "total_loss_usd": 65_000_000_000,
        "victims_count": 4800,
        "duration_years": 17,
        "geographic_impact": "global"
    },
    CaseType.LTCM: {
        "total_loss_usd": 4_600_000_000,
        "leverage_ratio": 25,
        "duration_months": 48,
        "systemic_risk": "high"
    },
    CaseType.LEHMAN: {
        "total_debt_usd": 613_000_000_000,
        "employees_affected": 25000,
        "company_age_years": 158,
        "global_impact": "financial_crisis"
    }
}

# =============================================================================
# UI THEME CONSTANTS
# =============================================================================

# Color themes for each role
COLOR_THEMES = {
    "blue": {
        "primary": "#1E3A8A",
        "secondary": "#3B82F6", 
        "accent": "#93C5FD",
        "background": "#EFF6FF",
        "text": "#1E40AF"
    },
    "red": {
        "primary": "#DC2626",
        "secondary": "#EF4444",
        "accent": "#FCA5A5", 
        "background": "#FEF2F2",
        "text": "#B91C1C"
    },
    "green": {
        "primary": "#059669",
        "secondary": "#10B981",
        "accent": "#6EE7B7",
        "background": "#F0FDF4", 
        "text": "#047857"
    },
    "cyan": {
        "primary": "#0891B2",
        "secondary": "#06B6D4",
        "accent": "#67E8F9",
        "background": "#F0F9FF",
        "text": "#0E7490"
    }
}

# Typography settings
TYPOGRAPHY = {
    "header_font": "Inter, sans-serif",
    "body_font": "Inter, sans-serif",
    "mono_font": "JetBrains Mono, monospace",
    "sizes": {
        "header_1": "2.5rem",
        "header_2": "2rem", 
        "header_3": "1.5rem",
        "body": "1rem",
        "small": "0.875rem"
    }
}

# =============================================================================
# MAGIC MOMENTS CONSTANTS
# =============================================================================

class MagicMomentType(Enum):
    """Types of magic moments in the experience"""
    REALITY_SHOCK = "reality_shock"
    DATA_REVEAL = "data_reveal"
    FRAMEWORK_CLICK = "framework_click"
    TOOL_GENERATION = "tool_generation"

# Magic moment configurations
MAGIC_MOMENTS = {
    MagicMomentType.REALITY_SHOCK: {
        "trigger_role": RoleType.INVESTOR,
        "duration_seconds": 3.0,
        "audio_cue": "warning_tone",
        "visual_effect": "color_flash_red",
        "text_effect": "bold_large"
    },
    MagicMomentType.DATA_REVEAL: {
        "trigger_role": RoleType.INVESTOR,
        "duration_seconds": 2.0,
        "audio_cue": "notification_chime",
        "visual_effect": "counter_animation",
        "text_effect": "highlight_numbers"
    },
    MagicMomentType.FRAMEWORK_CLICK: {
        "trigger_role": RoleType.MENTOR,
        "duration_seconds": 1.5,
        "audio_cue": "soft_chime",
        "visual_effect": "gentle_glow",
        "text_effect": "emphasis_fade_in"
    },
    MagicMomentType.TOOL_GENERATION: {
        "trigger_role": RoleType.ASSISTANT,
        "duration_seconds": 4.0,
        "audio_cue": "success_melody",
        "visual_effect": "creation_animation",
        "text_effect": "typewriter_effect"
    }
}

# =============================================================================
# API CONSTANTS
# =============================================================================

# API model configurations
API_MODELS = {
    "gemini": {
        "primary": "gemini-2.0-flash-exp",
        "fallback": "gemini-1.5-pro",
        "max_tokens": 4000,
        "temperature": 0.7
    },
    "anthropic": {
        "primary": "claude-3-5-sonnet-20241022",
        "fallback": "claude-3-haiku-20240307", 
        "max_tokens": 4000,
        "temperature": 0.7
    }
}

# Rate limiting
API_RATE_LIMITS = {
    "requests_per_minute": 60,
    "requests_per_hour": 1000,
    "max_concurrent": 5
}

# Timeout settings
API_TIMEOUTS = {
    "connection_timeout": 10,
    "read_timeout": 30,
    "total_timeout": 45
}

# =============================================================================
# SESSION CONSTANTS
# =============================================================================

# Session state keys
SESSION_KEYS = {
    # Core session data
    "user_id": "user_id",
    "session_start": "session_start",
    "current_step": "current_step",
    "current_role": "current_role",
    "case_name": "case_name",
    
    # User interaction data
    "conversation_history": "conversation_history",
    "user_inputs": "user_inputs",
    "personalization_active": "personalization_active",
    
    # Generated content
    "generated_tools": "generated_tools",
    "magic_moments_triggered": "magic_moments_triggered",
    
    # System tracking
    "api_call_count": "api_call_count",
    "error_history": "error_history",
    "performance_metrics": "performance_metrics"
}

# Session limits
SESSION_LIMITS = {
    "max_duration_minutes": 45,
    "max_api_calls": 100,
    "max_conversation_turns": 50,
    "max_user_inputs": 20,
    "max_error_history": 10
}

# =============================================================================
# VALIDATION CONSTANTS
# =============================================================================

# Input validation patterns
VALIDATION_PATTERNS = {
    "company_name": r"^[a-zA-Z0-9\s\-\.]{2,50}$",
    "investment_amount": r"^[0-9\.\,万千亿百万]+$",
    "user_id": r"^[a-zA-Z0-9\-]{8,36}$"
}

# Input length limits
INPUT_LIMITS = {
    "company_name": {"min": 2, "max": 50},
    "investment_amount": {"min": 1, "max": 20},
    "decision_context": {"min": 10, "max": 500},
    "user_reflection": {"min": 20, "max": 1000}
}

# =============================================================================
# ERROR CONSTANTS
# =============================================================================

class ErrorType(Enum):
    """Error types for categorization"""
    API_ERROR = "api_error"
    VALIDATION_ERROR = "validation_error"
    SESSION_ERROR = "session_error"
    CONFIGURATION_ERROR = "config_error"
    SYSTEM_ERROR = "system_error"

# Error messages
ERROR_MESSAGES = {
    ErrorType.API_ERROR: "API service temporarily unavailable",
    ErrorType.VALIDATION_ERROR: "Input validation failed",
    ErrorType.SESSION_ERROR: "Session management error",
    ErrorType.CONFIGURATION_ERROR: "Configuration error",
    ErrorType.SYSTEM_ERROR: "System error occurred"
}

# =============================================================================
# PERFORMANCE CONSTANTS
# =============================================================================

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "api_response_time_ms": 5000,
    "page_load_time_ms": 2000,
    "session_init_time_ms": 1000,
    "role_switch_time_ms": 500
}

# Cache settings
CACHE_SETTINGS = {
    "default_ttl_seconds": 3600,
    "max_cache_size": 1000,
    "cache_cleanup_interval": 300
}

# =============================================================================
# FEATURE FLAGS
# =============================================================================

class FeatureFlag(Enum):
    """Available feature flags"""
    EXPERIMENTAL_UI = "experimental_ui"
    ADVANCED_ANALYTICS = "advanced_analytics"
    AUDIO_EFFECTS = "audio_effects"
    CUSTOM_THEMES = "custom_themes"
    EXPORT_TOOLS = "export_tools"

# Default feature flag values
DEFAULT_FEATURE_FLAGS = {
    FeatureFlag.EXPERIMENTAL_UI: False,
    FeatureFlag.ADVANCED_ANALYTICS: False,
    FeatureFlag.AUDIO_EFFECTS: True,
    FeatureFlag.CUSTOM_THEMES: False,
    FeatureFlag.EXPORT_TOOLS: True
}

# =============================================================================
# UTILITY CONSTANTS
# =============================================================================

# Date formats
DATE_FORMATS = {
    "iso": "%Y-%m-%dT%H:%M:%S.%fZ",
    "display": "%Y-%m-%d %H:%M:%S",
    "filename": "%Y%m%d_%H%M%S"
}

# File extensions
ALLOWED_FILE_EXTENSIONS = [".json", ".csv", ".txt", ".md"]

# URL patterns
URL_PATTERNS = {
    "github_repo": r"^https://github\.com/[\w\-\.]+/[\w\-\.]+$",
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_role_by_step(step: int) -> RoleType:
    """Get role type by step number"""
    role_map = {1: RoleType.HOST, 2: RoleType.INVESTOR, 3: RoleType.MENTOR, 4: RoleType.ASSISTANT}
    return role_map.get(step, RoleType.HOST)

def get_step_by_role(role: RoleType) -> int:
    """Get step number by role type"""
    for role_type, config in ROLE_CONFIG.items():
        if role_type == role:
            return config["step"]
    return 1

def get_color_theme(role: RoleType) -> Dict[str, str]:
    """Get color theme for a role"""
    theme_name = ROLE_CONFIG[role]["color_theme"]
    return COLOR_THEMES[theme_name]

def is_valid_case_type(case_name: str) -> bool:
    """Check if case name is valid"""
    return case_name in [case.value for case in CaseType]

def get_magic_moment_config(moment_type: MagicMomentType) -> Dict[str, Any]:
    """Get configuration for a magic moment"""
    return MAGIC_MOMENTS.get(moment_type, {})
