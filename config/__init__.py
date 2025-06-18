"""
Cognitive Black Box - Configuration Module Package
Manages case configurations and AI prompts based on S's Schema design
"""

__version__ = "2.0.0"
__author__ = "Claude (C) - Architecture Team"
__description__ = "Configuration management for cases and AI prompts"

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configuration paths
CONFIG_DIR = Path(__file__).parent
CASES_DIR = CONFIG_DIR / "cases"
PROMPTS_DIR = CONFIG_DIR / "prompts"

def get_app_config():
    """Get application configuration"""
    return {
        'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() == 'true',
        'show_debug_ui': os.getenv('SHOW_DEBUG_UI', 'false').lower() == 'true',
        'ai_enabled': os.getenv('AI_ENABLED', 'true').lower() == 'true',
        'fallback_mode': os.getenv('FALLBACK_MODE', 'false').lower() == 'true'
    }

def list_available_cases() -> List[str]:
    """List all available case configuration files"""
    try:
        if not CASES_DIR.exists():
            return []
        
        case_files = list(CASES_DIR.glob("*.json"))
        return [f.stem for f in case_files]
    except Exception:
        return []

def list_available_prompts() -> List[str]:
    """List all available AI prompt configuration files"""
    try:
        if not PROMPTS_DIR.exists():
            return []
        
        prompt_files = list(PROMPTS_DIR.glob("*.json"))
        return [f.stem for f in prompt_files]
    except Exception:
        return []

def load_case_config(case_id: str) -> Optional[Dict[str, Any]]:
    """Load case configuration file"""
    try:
        case_file = CASES_DIR / f"{case_id}.json"
        if not case_file.exists():
            return None
        
        with open(case_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def load_prompt_config(role_id: str) -> Optional[Dict[str, Any]]:
    """Load AI prompt configuration file"""
    try:
        prompt_file = PROMPTS_DIR / f"{role_id}.json"
        if not prompt_file.exists():
            return None
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def validate_case_schema(case_data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Validate case data against S's schema"""
    errors = []
    
    # Check required top-level fields
    required_fields = ['case_metadata', 'acts']
    for field in required_fields:
        if field not in case_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate case_metadata
    if 'case_metadata' in case_data:
        metadata = case_data['case_metadata']
        required_metadata = ['case_id', 'title', 'target_bias']
        
        for field in required_metadata:
            if field not in metadata:
                errors.append(f"Missing metadata field: {field}")
    
    # Validate acts structure
    if 'acts' in case_data:
        acts = case_data['acts']
        if not isinstance(acts, list):
            errors.append("'acts' must be a list")
        else:
            for i, act in enumerate(acts):
                if not isinstance(act, dict):
                    errors.append(f"Act {i} must be a dictionary")
                    continue
                
                required_act_fields = ['act_id', 'act_name', 'role', 'components']
                for field in required_act_fields:
                    if field not in act:
                        errors.append(f"Missing field '{field}' in act {i}")
                
                # Validate components
                if 'components' in act:
                    components = act['components']
                    if not isinstance(components, list):
                        errors.append(f"Components in act {i} must be a list")
                    else:
                        for j, component in enumerate(components):
                            if not isinstance(component, dict):
                                errors.append(f"Component {j} in act {i} must be a dictionary")
                            elif 'component_type' not in component:
                                errors.append(f"Component {j} in act {i} missing 'component_type'")
    
    return len(errors) == 0, errors

def get_config_status() -> Dict[str, Any]:
    """Get comprehensive configuration status"""
    status = {
        'config_dir_exists': CONFIG_DIR.exists(),
        'cases_dir_exists': CASES_DIR.exists(),
        'prompts_dir_exists': PROMPTS_DIR.exists(),
        'available_cases': list_available_cases(),
        'available_prompts': list_available_prompts(),
        'app_config': get_app_config()
    }
    
    # Validate key configurations
    status['madoff_case_valid'] = False
    status['all_prompts_available'] = False
    
    # Check madoff case
    madoff_config = load_case_config('madoff')
    if madoff_config:
        is_valid, errors = validate_case_schema(madoff_config)
        status['madoff_case_valid'] = is_valid
        if not is_valid:
            status['madoff_validation_errors'] = errors
    
    # Check AI prompts
    required_prompts = ['host', 'investor', 'mentor', 'assistant']
    available_prompts = list_available_prompts()
    status['all_prompts_available'] = all(prompt in available_prompts for prompt in required_prompts)
    status['missing_prompts'] = [prompt for prompt in required_prompts if prompt not in available_prompts]
    
    return status

def create_default_directories():
    """Create default configuration directories if they don't exist"""
    try:
        CASES_DIR.mkdir(parents=True, exist_ok=True)
        PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

def get_schema_info():
    """Get information about the current schema version"""
    return {
        'schema_version': '2.0.0',
        'based_on_design_by': 'Hoshino (S)',
        'implemented_by': 'Claude (C)',
        'supports_ai_integration': True,
        'supports_component_rendering': True,
        'supports_magic_moments': True,
        'supports_personalization': True
    }

# Export main functions
__all__ = [
    'get_app_config',
    'list_available_cases',
    'list_available_prompts', 
    'load_case_config',
    'load_prompt_config',
    'validate_case_schema',
    'get_config_status',
    'create_default_directories',
    'get_schema_info',
    'CONFIG_DIR',
    'CASES_DIR', 
    'PROMPTS_DIR'
]
