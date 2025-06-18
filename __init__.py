"""
Cognitive Black Box - Main Package
AI-powered cognitive bias experience platform

Architecture: Modular + Configurable + AI-Intelligent
Based on S's component schema design and C's technical architecture
"""

__version__ = "2.0.0"
__title__ = "Cognitive Black Box"
__author__ = "Team: Hoshino (S) + Claude (C)"
__description__ = "18分钟认知升级体验 - AI智能化决策训练平台"
__url__ = "https://cognitive-blackbox.streamlit.app"

# Package metadata
__license__ = "MIT"
__copyright__ = "2025 Cognitive Black Box Team"

# Import key components for easy access
try:
    # Core functionality
    from core import case_manager, ai_engine, get_module_status as get_core_status
    from utils import input_validator, error_handler, get_module_status as get_utils_status
    from views import component_renderer, get_module_status as get_views_status
    from config import get_app_config, get_config_status, get_schema_info
    
    _PACKAGE_LOADED = True
    _IMPORT_ERRORS = []
    
except ImportError as e:
    _PACKAGE_LOADED = False
    _IMPORT_ERRORS = [str(e)]
    
    # Provide minimal fallback functionality
    class _FallbackSystem:
        def __init__(self):
            self.available = False
            self.error = "Package modules not available"
    
    case_manager = _FallbackSystem()
    ai_engine = _FallbackSystem()
    input_validator = _FallbackSystem()
    error_handler = _FallbackSystem()
    component_renderer = _FallbackSystem()
    
    def get_app_config():
        return {'fallback_mode': True}
    
    def get_config_status():
        return {'status': 'error', 'message': 'Config module not available'}
    
    def get_schema_info():
        return {'schema_version': 'unknown', 'status': 'error'}

# Main exports
__all__ = [
    # Core components
    'case_manager',
    'ai_engine', 
    'input_validator',
    'error_handler',
    'component_renderer',
    
    # Configuration functions
    'get_app_config',
    'get_config_status',
    'get_schema_info',
    
    # System functions
    'get_system_status',
    'get_version_info',
    'validate_installation'
]

def get_system_status():
    """Get comprehensive system status"""
    status = {
        'package_version': __version__,
        'package_loaded': _PACKAGE_LOADED,
        'timestamp': None
    }
    
    if _PACKAGE_LOADED:
        try:
            from datetime import datetime
            status['timestamp'] = datetime.now().isoformat()
            
            # Get module statuses
            status['core'] = get_core_status()
            status['utils'] = get_utils_status()  
            status['views'] = get_views_status()
            status['config'] = get_config_status()
            
            # Overall health check
            core_ok = status['core'].get('status') == 'success'
            utils_ok = status['utils'].get('core_utils_loaded', False)
            views_ok = status['views'].get('status') == 'success'
            config_ok = status['config'].get('config_dir_exists', False)
            
            status['overall_health'] = 'healthy' if all([core_ok, utils_ok, views_ok, config_ok]) else 'degraded'
            status['critical_issues'] = []
            
            if not core_ok:
                status['critical_issues'].append('Core modules failed to load')
            if not utils_ok:
                status['critical_issues'].append('Utils modules failed to load')
            if not views_ok:
                status['critical_issues'].append('Views modules failed to load')
            if not config_ok:
                status['critical_issues'].append('Configuration directories missing')
                
        except Exception as e:
            status['status_check_error'] = str(e)
            status['overall_health'] = 'critical'
    else:
        status['overall_health'] = 'critical'
        status['import_errors'] = _IMPORT_ERRORS
    
    return status

def get_version_info():
    """Get detailed version information"""
    return {
        'version': __version__,
        'title': __title__,
        'description': __description__,
        'author': __author__,
        'url': __url__,
        'license': __license__,
        'copyright': __copyright__,
        'package_loaded': _PACKAGE_LOADED,
        'architecture': 'modular + configurable + AI-intelligent',
        'schema_version': get_schema_info().get('schema_version', 'unknown')
    }

def validate_installation():
    """Validate complete installation"""
    validation = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'recommendations': []
    }
    
    try:
        # Check package loading
        if not _PACKAGE_LOADED:
            validation['valid'] = False
            validation['errors'].extend(_IMPORT_ERRORS)
            validation['recommendations'].append("Run: pip install -r requirements.txt")
        
        # Check system status
        system_status = get_system_status()
        
        if system_status.get('overall_health') == 'critical':
            validation['valid'] = False
            validation['errors'].extend(system_status.get('critical_issues', []))
        
        elif system_status.get('overall_health') == 'degraded':
            validation['warnings'].extend(system_status.get('critical_issues', []))
        
        # Check configuration
        config_status = get_config_status()
        
        if not config_status.get('madoff_case_valid', False):
            validation['warnings'].append("Madoff case configuration invalid or missing")
            validation['recommendations'].append("Ensure config/cases/madoff.json exists and is valid")
        
        if not config_status.get('all_prompts_available', False):
            missing = config_status.get('missing_prompts', [])
            validation['warnings'].append(f"Missing AI prompt configs: {missing}")
            validation['recommendations'].append("Ensure all prompt files exist in config/prompts/")
        
        # Check AI functionality
        try:
            if hasattr(ai_engine, 'get_available_apis'):
                available_apis = ai_engine.get_available_apis()
                if not available_apis:
                    validation['warnings'].append("No AI APIs available")
                    validation['recommendations'].append("Configure GEMINI_API_KEY or ANTHROPIC_API_KEY")
        except:
            validation['warnings'].append("AI engine status check failed")
    
    except Exception as e:
        validation['valid'] = False
        validation['errors'].append(f"Validation check failed: {str(e)}")
    
    return validation

def quick_start_check():
    """Quick check for immediate usability"""
    try:
        # Test basic functionality
        validation = validate_installation()
        
        if validation['valid'] and not validation['errors']:
            return {
                'ready': True,
                'message': "✅ Cognitive Black Box is ready to run!",
                'next_step': "Run: streamlit run app.py"
            }
        elif not validation['errors']:
            return {
                'ready': True,
                'message': "⚠️ System ready with some warnings",
                'warnings': validation['warnings'],
                'next_step': "Run: streamlit run app.py (functionality may be limited)"
            }
        else:
            return {
                'ready': False,
                'message': "❌ System not ready",
                'errors': validation['errors'],
                'recommendations': validation['recommendations']
            }
    except Exception as e:
        return {
            'ready': False,
            'message': f"❌ Quick start check failed: {str(e)}",
            'recommendations': ["Check installation and try again"]
        }
