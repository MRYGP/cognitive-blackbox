"""
Cognitive Black Box - Case Management System
Handles loading, validation, and management of case configuration files
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

@dataclass
class ActContent:
    """Act content structure"""
    theme_color: str
    role: str
    title: str
    progress: int
    opening_quote: str
    knowledge_card: Dict[str, Any]
    content: Dict[str, Any]

class CaseManager:
    """
    Case configuration manager
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
            
            # Validate case data
            if not self._validate_case_data(case_data):
                self.logger.error(f"Invalid case data structure: {case_id}")
                return None
            
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
    
    def _validate_case_data(self, case_data: Dict[str, Any]) -> bool:
        """
        Validate case data structure
        
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
        
        # Check acts structure
        acts = case_data['acts']
        required_acts = ['act1_host', 'act2_investor', 'act3_mentor', 'act4_assistant']
        
        for act in required_acts:
            if act not in acts:
                self.logger.error(f"Missing act: {act}")
                return False
        
        return True
    
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
            return CaseMetadata(
                case_id=metadata['case_id'],
                title=metadata['title'],
                target_bias=metadata['target_bias'],
                duration_minutes=metadata['duration_minutes'],
                target_user=metadata.get('target_user', ''),
                difficulty_level=metadata.get('difficulty_level', 'advanced'),
                financial_impact=metadata.get('financial_impact', {})
            )
        except Exception as e:
            self.logger.error(f"Error parsing metadata for case '{case_id}': {str(e)}")
            return None
    
    def get_act_content(self, case_id: str, act_id: str) -> Optional[Dict[str, Any]]:
        """
        Get content for specific act
        
        Args:
            case_id: Case identifier
            act_id: Act identifier (e.g., 'act1_host')
        
        Returns:
            Dict containing act content, None if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return None
        
        acts = case_data.get('acts', {})
        if act_id not in acts:
            self.logger.error(f"Act '{act_id}' not found in case '{case_id}'")
            return None
        
        return acts[act_id]
    
    def get_decision_points(self, case_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get decision points for Act 1
        
        Args:
            case_id: Case identifier
        
        Returns:
            List of decision points, None if failed
        """
        act1_content = self.get_act_content(case_id, 'act1_host')
        if not act1_content:
            return None
        
        return act1_content.get('decision_points', [])
    
    def get_challenges(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Get challenges for Act 2
        
        Args:
            case_id: Case identifier
        
        Returns:
            Dict containing challenges, None if failed
        """
        act2_content = self.get_act_content(case_id, 'act2_investor')
        if not act2_content:
            return None
        
        return act2_content.get('four_challenges', {})
    
    def get_framework_content(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Get framework content for Act 3
        
        Args:
            case_id: Case identifier
        
        Returns:
            Dict containing framework content, None if failed
        """
        act3_content = self.get_act_content(case_id, 'act3_mentor')
        if not act3_content:
            return None
        
        return act3_content.get('framework_solution', {})
    
    def get_personalization_config(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Get personalization configuration
        
        Args:
            case_id: Case identifier
        
        Returns:
            Dict containing personalization config, None if failed
        """
        case_data = self.load_case(case_id)
        if not case_data:
            return None
        
        return case_data.get('personalization', {})
    
    def get_magic_moments(self, case_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get magic moments configuration
        
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
            'available_cases': self.get_available_cases()
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
    Case content renderer
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
    
    def render_act_header(self, case_id: str, act_id: str) -> None:
        """
        Render act header with theme
        
        Args:
            case_id: Case identifier
            act_id: Act identifier
        """
        act_content = self.case_manager.get_act_content(case_id, act_id)
        if not act_content:
            st.error(f"Failed to load content for {act_id}")
            return
        
        # Set theme
        theme_color = act_content.get('theme_color', 'blue')
        
        # Render header
        st.header(act_content.get('title', f'Act {act_id[-1]}'))
        st.progress(act_content.get('progress', 0))
        
        # Render quote if available
        if 'opening_quote' in act_content:
            st.info(act_content['opening_quote'])
    
    def render_knowledge_card(self, case_id: str, act_id: str) -> None:
        """
        Render knowledge card sidebar
        
        Args:
            case_id: Case identifier
            act_id: Act identifier
        """
        act_content = self.case_manager.get_act_content(case_id, act_id)
        if not act_content or 'knowledge_card' not in act_content:
            return
        
        knowledge_card = act_content['knowledge_card']
        
        with st.sidebar:
            st.subheader(knowledge_card.get('title', 'Knowledge'))
            
            content = knowledge_card.get('content', [])
            if isinstance(content, list):
                for item in content:
                    st.write(item)
            else:
                st.write(content)
    
    def render_css_theme(self, theme_color: str) -> None:
        """
        Inject CSS for theme
        
        Args:
            theme_color: Theme color name
        """
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
