"""
Cognitive Black Box - Utilities Package
Contains session management, AI roles, and data models
"""

from .session_manager import session_manager
from .ai_roles import ai_engine  
from .data_models import CaseType, RoleType, CaseSession, create_case_session

__all__ = [
    'session_manager',
    'ai_engine', 
    'CaseType',
    'RoleType', 
    'CaseSession',
    'create_case_session'
]
