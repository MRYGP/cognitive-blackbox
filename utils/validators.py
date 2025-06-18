"""
Cognitive Black Box - Input Validation Utilities
Provides comprehensive validation for user inputs and system data
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
import logging

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)

class InputValidator:
    """
    Comprehensive input validation system
    """
    
    def __init__(self):
        """Initialize validator with patterns and rules"""
        self.logger = logging.getLogger(__name__)
        
        # Validation patterns
        self.patterns = {
            'company_name': re.compile(r'^[\u4e00-\u9fff\w\s\.\-&（）()]{2,50}$'),
            'investment_amount': re.compile(r'^[\d\.\,万千亿百万元美金人民币USD￥$\s]{1,50}$'),
            'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            'user_id': re.compile(r'^[a-zA-Z0-9\-_]{8,36}$'),
            'case_id': re.compile(r'^[a-z]{3,20}$'),
            'role_id': re.compile(r'^(host|investor|mentor|assistant)$')
        }
        
        # Length limits
        self.length_limits = {
            'company_name': {'min': 2, 'max': 50},
            'investment_amount': {'min': 1, 'max': 50},
            'decision_context': {'min': 5, 'max': 1000},
            'user_reflection': {'min': 10, 'max': 2000},
            'system_name': {'min': 3, 'max': 30},
            'core_principle': {'min': 5, 'max': 100}
        }
        
        # Forbidden patterns (security)
        self.forbidden_patterns = [
            re.compile(r'<script', re.IGNORECASE),
            re.compile(r'javascript:', re.IGNORECASE),
            re.compile(r'onclick', re.IGNORECASE),
            re.compile(r'onerror', re.IGNORECASE),
            re.compile(r'onload', re.IGNORECASE),
            re.compile(r'eval\(', re.IGNORECASE),
            re.compile(r'document\.', re.IGNORECASE)
        ]
    
    def validate_user_input(self, input_type: str, value: str, required: bool = True) -> Tuple[bool, str]:
        """
        Validate user input based on type
        
        Args:
            input_type: Type of input (company_name, investment_amount, etc.)
            value: Input value to validate
            required: Whether the field is required
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Check if value is provided for required fields
            if required and (not value or not value.strip()):
                return False, f"{input_type} is required"
            
            # If not required and empty, it's valid
            if not required and (not value or not value.strip()):
                return True, ""
            
            # Clean the value
            cleaned_value = value.strip()
            
            # Security check - prevent XSS and injection
            if self._contains_forbidden_patterns(cleaned_value):
                return False, "Input contains forbidden content"
            
            # Length validation
            if not self._validate_length(input_type, cleaned_value):
                limits = self.length_limits.get(input_type, {'min': 1, 'max': 100})
                return False, f"Length must be between {limits['min']} and {limits['max']} characters"
            
            # Pattern validation
            if input_type in self.patterns:
                if not self.patterns[input_type].match(cleaned_value):
                    return False, f"Invalid format for {input_type}"
            
            # Content-specific validation
            if input_type == 'investment_amount':
                return self._validate_investment_amount(cleaned_value)
            elif input_type == 'company_name':
                return self._validate_company_name(cleaned_value)
            elif input_type == 'decision_context':
                return self._validate_decision_context(cleaned_value)
            
            return True, ""
            
        except Exception as e:
            self.logger.error(f"Validation error for {input_type}: {str(e)}")
            return False, "Validation failed due to internal error"
    
    def validate_session_data(self, session_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate session data structure
        
        Args:
            session_data: Session data to validate
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            # Required session fields
            required_fields = ['user_id', 'case_name', 'current_step']
            
            for field in required_fields:
                if field not in session_data:
                    errors.append(f"Missing required field: {field}")
                    continue
                
                # Validate specific fields
                if field == 'user_id':
                    if not self.patterns['user_id'].match(session_data[field]):
                        errors.append("Invalid user_id format")
                
                elif field == 'case_name':
                    if not self.patterns['case_id'].match(session_data[field]):
                        errors.append("Invalid case_name format")
                
                elif field == 'current_step':
                    if not isinstance(session_data[field], int) or not 1 <= session_data[field] <= 4:
                        errors.append("current_step must be integer between 1 and 4")
            
            # Validate current_role if present
            if 'current_role' in session_data:
                if not self.patterns['role_id'].match(session_data['current_role']):
                    errors.append("Invalid current_role")
            
            # Validate user_inputs if present
            if 'user_inputs' in session_data and isinstance(session_data['user_inputs'], dict):
                for input_type, input_value in session_data['user_inputs'].items():
                    if isinstance(input_value, str):
                        is_valid, error_msg = self.validate_user_input(input_type, input_value, False)
                        if not is_valid:
                            errors.append(f"Invalid user_input[{input_type}]: {error_msg}")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Session validation error: {str(e)}")
            return False, ["Session validation failed due to internal error"]
    
    def validate_case_config(self, config_path: Union[str, Path]) -> Tuple[bool, List[str]]:
        """
        Validate case configuration file
        
        Args:
            config_path: Path to case configuration file
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            config_path = Path(config_path)
            
            # Check if file exists
            if not config_path.exists():
                return False, [f"Configuration file not found: {config_path}"]
            
            # Load and parse JSON
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            except json.JSONDecodeError as e:
                return False, [f"Invalid JSON format: {str(e)}"]
            
            # Validate structure
            required_top_level = ['case_metadata', 'acts']
            for field in required_top_level:
                if field not in config_data:
                    errors.append(f"Missing required field: {field}")
            
            # Validate case_metadata
            if 'case_metadata' in config_data:
                metadata_errors = self._validate_case_metadata(config_data['case_metadata'])
                errors.extend(metadata_errors)
            
            # Validate acts
            if 'acts' in config_data:
                acts_errors = self._validate_acts_structure(config_data['acts'])
                errors.extend(acts_errors)
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Case config validation error: {str(e)}")
            return False, ["Case configuration validation failed due to internal error"]
    
    def _contains_forbidden_patterns(self, value: str) -> bool:
        """Check if value contains forbidden security patterns"""
        for pattern in self.forbidden_patterns:
            if pattern.search(value):
                return True
        return False
    
    def _validate_length(self, input_type: str, value: str) -> bool:
        """Validate input length"""
        if input_type not in self.length_limits:
            return True  # No specific limit
        
        limits = self.length_limits[input_type]
        return limits['min'] <= len(value) <= limits['max']
    
    def _validate_investment_amount(self, value: str) -> Tuple[bool, str]:
        """Validate investment amount format"""
        # Remove common formatting
        cleaned = re.sub(r'[,，\s]', '', value)
        
        # Check for Chinese currency units
        chinese_units = ['万', '千', '亿', '百万', '元', '人民币']
        has_chinese_unit = any(unit in cleaned for unit in chinese_units)
        
        # Check for English currency units
        english_units = ['USD', 'usd', '$', '美金', 'million', 'billion']
        has_english_unit = any(unit in cleaned.lower() for unit in english_units)
        
        # Must have at least one digit
        if not re.search(r'\d', cleaned):
            return False, "Investment amount must contain numbers"
        
        # Should have currency context
        if not (has_chinese_unit or has_english_unit):
            # Allow if it's just numbers (assume it's in standard units)
            if re.match(r'^\d+(\.\d+)?$', cleaned):
                return True, ""
            return False, "Investment amount should specify currency unit"
        
        return True, ""
    
    def _validate_company_name(self, value: str) -> Tuple[bool, str]:
        """Validate company name"""
        # Check for reasonable company name patterns
        if len(value) < 2:
            return False, "Company name too short"
        
        # Should not be all numbers
        if value.isdigit():
            return False, "Company name cannot be only numbers"
        
        # Check for suspicious patterns
        suspicious_words = ['test', 'TEST', '测试', 'demo', 'DEMO']
        if value.lower() in [w.lower() for w in suspicious_words]:
            return False, "Please enter a real company name"
        
        return True, ""
    
    def _validate_decision_context(self, value: str) -> Tuple[bool, str]:
        """Validate decision context"""
        # Should be meaningful content
        if len(value.split()) < 3:
            return False, "Decision context should be more descriptive"
        
        # Check for copy-paste patterns
        if value.count('\n') > 5:
            return False, "Decision context appears to be copied content"
        
        return True, ""
    
    def _validate_case_metadata(self, metadata: Dict[str, Any]) -> List[str]:
        """Validate case metadata structure"""
        errors = []
        
        required_fields = ['case_id', 'title', 'target_bias', 'duration_minutes']
        for field in required_fields:
            if field not in metadata:
                errors.append(f"Missing metadata field: {field}")
        
        # Validate specific fields
        if 'case_id' in metadata:
            if not isinstance(metadata['case_id'], str) or not self.patterns['case_id'].match(metadata['case_id']):
                errors.append("Invalid case_id format")
        
        if 'duration_minutes' in metadata:
            if not isinstance(metadata['duration_minutes'], int) or metadata['duration_minutes'] <= 0:
                errors.append("duration_minutes must be positive integer")
        
        return errors
    
    def _validate_acts_structure(self, acts: Dict[str, Any]) -> List[str]:
        """Validate acts structure"""
        errors = []
        
        required_acts = ['act1_host', 'act2_investor', 'act3_mentor', 'act4_assistant']
        for act in required_acts:
            if act not in acts:
                errors.append(f"Missing act: {act}")
            else:
                # Validate act structure
                act_data = acts[act]
                if not isinstance(act_data, dict):
                    errors.append(f"Act {act} must be a dictionary")
                    continue
                
                # Check required act fields
                required_act_fields = ['role', 'title', 'theme_color']
                for field in required_act_fields:
                    if field not in act_data:
                        errors.append(f"Missing field {field} in {act}")
        
        return errors

class SchemaValidator:
    """
    Validate data against predefined schemas
    """
    
    @staticmethod
    def validate_prompt_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate AI prompt configuration"""
        errors = []
        
        required_fields = ['role_id', 'name', 'system_prompt']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate role_id
        if 'role_id' in config:
            valid_roles = ['host', 'investor', 'mentor', 'assistant']
            if config['role_id'] not in valid_roles:
                errors.append(f"Invalid role_id. Must be one of: {valid_roles}")
        
        # Validate system_prompt length
        if 'system_prompt' in config:
            if len(config['system_prompt']) < 50:
                errors.append("system_prompt too short (minimum 50 characters)")
            elif len(config['system_prompt']) > 5000:
                errors.append("system_prompt too long (maximum 5000 characters)")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_magic_moment(moment: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate magic moment configuration"""
        errors = []
        
        required_fields = ['name', 'trigger_step', 'description']
        for field in required_fields:
            if field not in moment:
                errors.append(f"Missing required field: {field}")
        
        # Validate trigger_step
        if 'trigger_step' in moment:
            if not isinstance(moment['trigger_step'], int) or not 1 <= moment['trigger_step'] <= 4:
                errors.append("trigger_step must be integer between 1 and 4")
        
        return len(errors) == 0, errors

# Global validator instance
input_validator = InputValidator()
schema_validator = SchemaValidator()
