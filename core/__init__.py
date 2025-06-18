"""
Cognitive Black Box - Core Module Package
Contains the core business logic and AI functionality
"""

__version__ = "2.0.0"
__author__ = "Claude (C) - Architecture Team"
__description__ = "Core modules for modular + configurable + AI-intelligent architecture"

# Import key classes for easy access
try:
    from .case_manager import case_manager, case_renderer, CaseManager, CaseRenderer
    from .ai_engine import ai_engine, EnhancedAIEngine, AIRole
    
    __all__ = [
        'case_manager',
        'case_renderer', 
        'CaseManager',
        'CaseRenderer',
        'ai_engine',
        'EnhancedAIEngine',
        'AIRole'
    ]
    
    # Module initialization success
    _CORE_MODULES_LOADED = True
    
except ImportError as e:
    # Graceful degradation if modules fail to load
    _CORE_MODULES_LOADED = False
    _IMPORT_ERROR = str(e)
    
    # Provide fallback empty classes to prevent complete failure
    class _FallbackManager:
        def __init__(self):
            self.available = False
            
        def load_case(self, case_id):
            return None
            
        def get_available_apis(self):
            return []
    
    # Export fallback instances
    case_manager = _FallbackManager()
    ai_engine = _FallbackManager()
    
    __all__ = ['case_manager', 'ai_engine']

def get_module_status():
    """Get status of core module loading"""
    if _CORE_MODULES_LOADED:
        return {
            'status': 'success',
            'message': 'All core modules loaded successfully',
            'available_modules': __all__
        }
    else:
        return {
            'status': 'error', 
            'message': f'Module loading failed: {_IMPORT_ERROR}',
            'fallback_active': True
        }

def get_version_info():
    """Get version information"""
    return {
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'modules_loaded': _CORE_MODULES_LOADED
    }
