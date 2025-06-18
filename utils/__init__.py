"""
Cognitive Black Box - Utilities Module Package
Contains validation, error handling, and utility functions
"""

__version__ = "2.0.0"
__author__ = "Claude (C) - Architecture Team"
__description__ = "Utility modules for input validation, error handling, and system support"

# Import utility classes and functions
try:
    from .validators import input_validator, schema_validator, InputValidator, SchemaValidator
    from .error_handlers import error_handler, error_handler_decorator, ErrorType, ErrorSeverity, ErrorInfo
    
    # Try to import existing modules (backward compatibility)
    try:
        from .session_manager import session_manager
        _SESSION_MANAGER_AVAILABLE = True
    except ImportError:
        _SESSION_MANAGER_AVAILABLE = False
        session_manager = None
    
    try:
        from .ai_roles import ai_engine as legacy_ai_engine
        _LEGACY_AI_AVAILABLE = True
    except ImportError:
        _LEGACY_AI_AVAILABLE = False
        legacy_ai_engine = None
    
    __all__ = [
        # New architecture modules
        'input_validator',
        'schema_validator',
        'InputValidator', 
        'SchemaValidator',
        'error_handler',
        'error_handler_decorator',
        'ErrorType',
        'ErrorSeverity',
        'ErrorInfo',
        # Legacy modules (if available)
        'session_manager',
        'legacy_ai_engine'
    ]
    
    # Remove None values from __all__
    __all__ = [item for item in __all__ if globals().get(item) is not None]
    
    _UTILS_MODULES_LOADED = True
    
except ImportError as e:
    # Graceful degradation
    _UTILS_MODULES_LOADED = False
    _IMPORT_ERROR = str(e)
    
    # Provide minimal fallback functionality
    class _FallbackValidator:
        def validate_user_input(self, input_type, value, required=True):
            return True, ""
        
        def validate_session_data(self, session_data):
            return True, []
    
    class _FallbackErrorHandler:
        def handle_error(self, exception, error_type, context=None, user_visible=True, auto_recover=True):
            print(f"Error occurred: {str(exception)}")
            return None
        
        def get_error_stats(self):
            return {'total_errors': 0}
    
    # Export fallback instances
    input_validator = _FallbackValidator()
    error_handler = _FallbackErrorHandler()
    
    __all__ = ['input_validator', 'error_handler']

def get_module_status():
    """Get status of utils module loading"""
    status = {
        'core_utils_loaded': _UTILS_MODULES_LOADED,
        'session_manager_available': _SESSION_MANAGER_AVAILABLE,
        'legacy_ai_available': _LEGACY_AI_AVAILABLE,
        'available_modules': __all__
    }
    
    if not _UTILS_MODULES_LOADED:
        status['error'] = _IMPORT_ERROR
        status['fallback_active'] = True
    
    return status

def get_compatibility_info():
    """Get backward compatibility information"""
    return {
        'new_architecture': _UTILS_MODULES_LOADED,
        'legacy_session_manager': _SESSION_MANAGER_AVAILABLE,
        'legacy_ai_roles': _LEGACY_AI_AVAILABLE,
        'migration_needed': _SESSION_MANAGER_AVAILABLE or _LEGACY_AI_AVAILABLE
    }

def validate_system_health():
    """Quick system health check"""
    health = {
        'validators': True,
        'error_handlers': True,
        'session_manager': _SESSION_MANAGER_AVAILABLE,
        'overall_status': 'healthy' if _UTILS_MODULES_LOADED else 'degraded'
    }
    
    try:
        # Test basic validator functionality
        test_result, _ = input_validator.validate_user_input('company_name', 'Test Company')
        health['validators'] = test_result
    except:
        health['validators'] = False
    
    try:
        # Test basic error handler functionality  
        stats = error_handler.get_error_stats()
        health['error_handlers'] = 'total_errors' in stats
    except:
        health['error_handlers'] = False
    
    # Update overall status
    if not (health['validators'] and health['error_handlers']):
        health['overall_status'] = 'critical'
    
    return health
