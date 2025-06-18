"""
Cognitive Black Box - Case Management System (Fixed for New Schema)
Handles loading, validation, and management of case configuration files
Updated to support S's new acts array schema
"""

import json
import streamlit as st
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
from dataclasses import dataclass

@dataclass
class CaseMetadata:
    """Case metadata structure"""
    case_id: str
    title: str
    target_bias: str
    duration_minutes: int
    target_user: str
    difficulty_level: str
    financial_impact: Dict[str, Any]

class CaseManager:
    """
    Case configuration manager (Updated for New Schema)
    Responsible for loading, validating, and managing case files
    """
    
    def __init__(self, cases_dir: str = "config/cases"):
        """
        Initialize case manager
        
        Args:
            cases_dir: Directory containing case configuration files
        """
        self.cases_dir = Path(cases_dir)
        self.loaded_cases = {}
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging for case management"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Load case configuration from JSON file
        
        Args:
            case_id: Case identifier (e.g., 'madoff', 'ltcm')
        
        Returns:
            Dict containing case configuration, None if failed
        """
        try:
            # Check cache first
            if case_id in self.loaded_cases:
                self.logger.info(f"Loading case '{case_id}' from cache")
                return self.loaded_cases[case_id]
            
            # Load from file
            case_file = self.cases_dir / f"{case_id}.json"
            
            if not case_file.exists():
                self.logger.error(f"Case file not found: {case_file}")
                return None
            
            with open(case_file, 'r', encoding='utf-8') as f:
                case_data = json.load(f)
            
            # Validate case data (NEW SCHEMA)
            if not self._validate_case_data_new_schema(case_data):
                self.logger.error(f"Invalid case data structure: {case_id}")
                return None
            
            # Transform to internal format if needed
            case_data = self._transform_case_data(case_data)
            
            # Cache the loaded case
            self.loaded_cases[case_id] = case_data
            self.logger.info(f"Successfully loaded case: {case_id}")
            
            return case_data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error in case '{case_id}': {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading case '{case_id}': {str(e)}")
            return None
    
    def _validate_case_data_new_schema(self, case_data: Dict[str, Any]) -> bool:
        """
        Validate case data structure (NEW SCHEMA SUPPORT)
        
        Args:
            case_data: Case configuration data
        
        Returns:
            bool: True if valid, False otherwise
        """
        required_keys = ['case_metadata', 'acts']
        
        # Check top-level structure
        for key in required_keys:
            if key not in case_data:
                self.logger.error(f"Missing required key: {key}")
                return False
        
        # Check case metadata
        metadata = case_data['case_metadata']
        required_metadata = ['case_id', 'title', 'target_bias', 'duration_minutes']
        
        for key in required_metadata:
            if key not in metadata:
                self.logger.error(f"Missing metadata key: {key}")
                return False
        
        # Check acts structure (NEW SCHEMA - array of acts)
        acts = case_data['acts']
        if not isinstance(acts, list):
            self.logger.error("Acts must be an array")
            return False
        
        # Validate each act has required fields
        required_act_fields = ['act_id', 'act_name', 'role', 'components']
        for i, act in enumerate(acts):
            for field in required_act_fields:
                if field not in act:
                    self.logger.error(f"Missing field '{field}' in act {i+1}")
                    return False
        
        # Check we have 4 acts (as expected for full experience)
        if len(acts) != 4:
            self.logger.warning(f"Expected 4 acts, found {len(acts)}")
        
        return True
    
    def _transform_case_data(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform new schema to internal format if needed
        
        Args:
            case_data: Case data in new schema format
        
        Returns:
            Transformed case data
        """
        # The new schema is already in the correct format for component_renderer
        # Just ensure acts are accessible by both array index and ID
        
        acts_array = case_data['acts']
        
        # Create acts lookup for backward compatibility
        acts_dict = {}
        for act in acts_array:
            act_id = act['act_id']
            role = act['role']
            
            # Create legacy key format
            legacy_key = f"act{act_id}_{role}"
            acts_dict[legacy_key] = act
        
        # Add both formats
        case_data['acts_array'] = acts_array  # New format for component_renderer
        case_data['acts_dict'] = acts_dict    # Legacy format for compatibility
        
        return case_data
    
    def get_case_metadata(self, case_id: str) -> Optional[CaseMetadata]:
        """
        Get case metadata as structured object
        
        Args:
            case_id: Case identifier
        
        Returns:
            CaseMetadata object or None if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return None
        
        try:
            metadata = case_data['case_metadata']
            
            # Handle target_bias which might be string or dict in new schema
            target_bias = metadata.get('target_bias', '')
            if isinstance(target_bias, dict):
                target_bias = target_bias.get('name_cn', target_bias.get('name_en', ''))
            
            return CaseMetadata(
                case_id=metadata['case_id'],
                title=metadata['title'],
                target_bias=target_bias,
                duration_minutes=metadata['duration_minutes'],
                target_user=metadata.get('target_user_profile', metadata.get('target_user', '')),
                difficulty_level=metadata.get('difficulty_level', 'advanced'),
                financial_impact=metadata.get('financial_impact', {})
            )
        except Exception as e:
            self.logger.error(f"Error parsing metadata for case '{case_id}': {str(e)}")
            return None
    
    def get_act_by_id(self, case_id: str, act_id: int) -> Optional[Dict[str, Any]]:
        """
        Get act by ID (NEW SCHEMA METHOD)
        
        Args:
            case_id: Case identifier
            act_id: Act ID (1, 2, 3, 4)
        
        Returns:
            Dict containing act content, None if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return None
        
        acts_array = case_data.get('acts_array', case_data.get('acts', []))
        
        for act in acts_array:
            if act.get('act_id') == act_id:
                return act
        
        self.logger.error(f"Act with ID '{act_id}' not found in case '{case_id}'")
        return None
    
    def get_act_content(self, case_id: str, act_id: str) -> Optional[Dict[str, Any]]:
        """
        Get content for specific act (LEGACY COMPATIBILITY)
        
        Args:
            case_id: Case identifier
            act_id: Act identifier (e.g., 'act1_host')
        
        Returns:
            Dict containing act content, None if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return None
        
        # Try legacy format first
        acts_dict = case_data.get('acts_dict', {})
        if act_id in acts_dict:
            return acts_dict[act_id]
        
        # Try to parse act_id format: "act{number}_{role}"
        try:
            if act_id.startswith('act') and '_' in act_id:
                parts = act_id.split('_')
                act_number = int(parts[0][3:])  # Extract number from "act1", "act2", etc.
                return self.get_act_by_id(case_id, act_number)
        except (ValueError, IndexError):
            pass
        
        self.logger.error(f"Act '{act_id}' not found in case '{case_id}'")
        return None
    
    def get_all_acts(self, case_id: str) -> List[Dict[str, Any]]:
        """
        Get all acts for a case (NEW SCHEMA METHOD)
        
        Args:
            case_id: Case identifier
        
        Returns:
            List of acts, empty list if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return []
        
        return case_data.get('acts_array', case_data.get('acts', []))
    
    def get_decision_points(self, case_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get decision points for Act 1 (UPDATED FOR NEW SCHEMA)
        
        Args:
            case_id: Case identifier
        
        Returns:
            List of decision points, None if failed
        """
        act1 = self.get_act_by_id(case_id, 1)
        if not act1:
            return None
        
        # Find decision_points component
        components = act1.get('components', [])
        for component in components:
            if component.get('component_type') == 'decision_points':
                return component.get('points', [])
        
        return None
    
    def get_ai_integration_config(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Get AI integration configuration (NEW SCHEMA METHOD)
        
        Args:
            case_id: Case identifier
        
        Returns:
            Dict containing AI config, None if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return None
        
        return case_data.get('ai_integration', {})
    
    def get_magic_moments(self, case_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get magic moments configuration (NEW SCHEMA METHOD)
        
        Args:
            case_id: Case identifier
        
        Returns:
            List of magic moments, None if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return None
        
        return case_data.get('magic_moments', [])
    
    def get_available_cases(self) -> List[str]:
        """
        Get list of available case IDs
        
        Returns:
            List of case identifiers
        """
        try:
            if not self.cases_dir.exists():
                self.logger.warning(f"Cases directory does not exist: {self.cases_dir}")
                return []
            
            case_files = list(self.cases_dir.glob("*.json"))
            return [f.stem for f in case_files]
            
        except Exception as e:
            self.logger.error(f"Error getting available cases: {str(e)}")
            return []
    
    def clear_cache(self) -> None:
        """Clear the case cache"""
        self.loaded_cases.clear()
        self.logger.info("Case cache cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get cache information
        
        Returns:
            Dict containing cache statistics
        """
        return {
            'cached_cases': list(self.loaded_cases.keys()),
            'cache_size': len(self.loaded_cases),
            'available_cases': self.get_available_cases(),
            'schema_version': '2.0.0'
        }
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def load_case_cached(_self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Load case with Streamlit caching
        
        Args:
            case_id: Case identifier
        
        Returns:
            Dict containing case configuration, None if failed
        """
        return _self.load_case(case_id)

class CaseRenderer:
    """
    Case content renderer (UPDATED FOR NEW SCHEMA)
    Handles rendering of case content with theme support
    """
    
    def __init__(self, case_manager: CaseManager):
        """
        Initialize case renderer
        
        Args:
            case_manager: CaseManager instance
        """
        self.case_manager = case_manager
        self.theme_colors = {
            'blue': '#1E3A8A',
            'red': '#DC2626', 
            'green': '#059669',
            'cyan': '#0891B2'
        }
    
    def render_act_header(self, case_id: str, act_id: int) -> None:
        """
        Render act header with theme (UPDATED FOR NEW SCHEMA)
        
        Args:
            case_id: Case identifier
            act_id: Act ID (1, 2, 3, 4)
        """
        act_content = self.case_manager.get_act_by_id(case_id, act_id)
        if not act_content:
            st.error(f"Failed to load content for act {act_id}")
            return
        
        # Set theme
        theme_color = act_content.get('theme_color_hex', '#2A52BE')
        
        # Render header
        st.header(act_content.get('act_name', f'Act {act_id}'))
        progress = act_content.get('progress_percentage', act_id * 25)
        st.progress(progress / 100)
        
        # Find and render opening quote from components
        components = act_content.get('components', [])
        for component in components:
            if component.get('component_type') == 'act_header':
                if 'opening_quote' in component:
                    st.info(component['opening_quote'])
                break
    
    def render_knowledge_card(self, case_id: str, act_id: int) -> None:
        """
        Render knowledge card sidebar (UPDATED FOR NEW SCHEMA)
        
        Args:
            case_id: Case identifier
            act_id: Act ID
        """
        act_content = self.case_manager.get_act_by_id(case_id, act_id)
        if not act_content:
            return
        
        # Find knowledge card component
        components = act_content.get('components', [])
        for component in components:
            if component.get('component_type') == 'knowledge_card':
                with st.sidebar:
                    st.subheader(component.get('title', 'Knowledge'))
                    
                    content_items = component.get('content_items', [])
                    for item in content_items:
                        st.write(item)
                break
    
    def render_css_theme(self, theme_color: str) -> None:
        """
        Inject CSS for theme
        
        Args:
            theme_color: Theme color name or hex
        """
        if theme_color.startswith('#'):
            color = theme_color
        else:
            color = self.theme_colors.get(theme_color, self.theme_colors['blue'])
        
        css = f"""
        <style>
        .role-container {{
            border-left: 6px solid {color};
            background-color: rgba({color.replace('#', '')}, 0.1);
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 12px;
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)

# Global instance
case_manager = CaseManager()
case_renderer = CaseRenderer(case_manager)
