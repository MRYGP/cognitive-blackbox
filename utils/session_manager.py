"""
Cognitive Black Box - Session State Management
Manages user session state, context switching, and data persistence
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from .data_models import CaseSession, CaseType, create_case_session, UserInput, ConversationTurn

class SessionManager:
    """
    Session state manager
    Responsible for managing user session lifecycle, context switching, and data persistence
    """
    
    def __init__(self):
        """Initialize session manager"""
        self.session_key = "cognitive_blackbox_session"
        self.backup_key = "session_backup"
        self.max_backup_count = 5
    
    def initialize_session(self, case_name: str = "madoff", user_id: str = None) -> bool:
        """
        Initialize new session
        
        Args:
            case_name: Case name ('madoff', 'ltcm', 'lehman')
            user_id: User identifier, auto-generate if not provided
        
        Returns:
            bool: Whether initialization was successful
        """
        try:
            # Generate user ID
            if not user_id:
                user_id = self._generate_user_id()
            
            # Validate case name
            if case_name not in ['madoff', 'ltcm', 'lehman']:
                st.error(f"Unsupported case: {case_name}")
                return False
            
            # Create case session
            case_type = CaseType(case_name)
            session = create_case_session(user_id, case_type)
            
            # Store in Streamlit session state
            st.session_state[self.session_key] = session
            
            # Initialize basic session state
            st.session_state.current_step = session.current_step
            st.session_state.current_role = session.current_role
            st.session_state.case_name = session.case_name
            st.session_state.user_id = session.user_id
            
            # Backup session
            self._backup_session(session)
            
            return True
            
        except Exception as e:
            st.error(f"Session initialization failed: {str(e)}")
            return False
    
    def get_current_session(self) -> Optional[CaseSession]:
        """Get current session"""
        return st.session_state.get(self.session_key, None)
    
    def get_current_context(self) -> Dict[str, Any]:
        """
        Get current context
        
        Returns:
            dict: Current session context information
        """
        session = self.get_current_session()
        if not session:
            return {}
        
        return session.get_current_context()
    
    def advance_step(self) -> bool:
        """
        Advance to next step
        
        Returns:
            bool: Whether step advancement was successful
        """
        session = self.get_current_session()
        if not session:
            st.error("No active session")
            return False
        
        try:
            success = session.advance_step()
            if success:
                # Update Streamlit session state
                st.session_state.current_step = session.current_step
                st.session_state.current_role = session.current_role
                
                # Backup session
                self._backup_session(session)
                
                return True
            else:
                st.warning("Cannot advance step: already at final step")
                return False
                
        except Exception as e:
            st.error(f"Step advancement failed: {str(e)}")
            return False
    
    def add_user_input(self, input_type: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Add user input
        
        Args:
            input_type: Input type
            content: Input content
            metadata: Additional metadata
        
        Returns:
            bool: Whether addition was successful
        """
        session = self.get_current_session()
        if not session:
            return False
        
        try:
            user_input = UserInput(
                input_type=input_type,
                content=content,
                metadata=metadata or {}
            )
            
            session.add_user_input(user_input)
            self._backup_session(session)
            
            return True
            
        except Exception as e:
            st.error(f"Failed to add user input: {str(e)}")
            return False
    
    def add_conversation_turn(self, role: str, message: str, user_input: UserInput = None, 
                           response_time: float = 0.0, api_used: str = "") -> bool:
        """
        Add conversation turn
        
        Args:
            role: Role name
            message: Message content
            user_input: Associated user input
            response_time: Response time
            api_used: API used
        
        Returns:
            bool: Whether addition was successful
        """
        session = self.get_current_session()
        if not session:
            return False
        
        try:
            turn = ConversationTurn(
                role=role,
                message=message,
                step=session.current_step,
                user_input=user_input,
                response_time=response_time,
                api_used=api_used
            )
            
            session.add_conversation_turn(turn)
            self._backup_session(session)
            
            return True
            
        except Exception as e:
            st.error(f"Failed to add conversation turn: {str(e)}")
            return False
    
    def trigger_magic_moment(self, moment_name: str) -> bool:
        """
        Trigger magic moment
        
        Args:
            moment_name: Magic moment name
        
        Returns:
            bool: Whether triggering was successful
        """
        session = self.get_current_session()
        if not session:
            return False
        
        success = session.trigger_magic_moment(moment_name)
        if success:
            self._backup_session(session)
        
        return success
    
    def enable_personalization(self) -> bool:
        """
        Enable personalization mode
        
        Returns:
            bool: Whether enabling was successful
        """
        session = self.get_current_session()
        if not session:
            return False
        
        session.personalization_active = True
        session.updated_at = datetime.now().isoformat()
        self._backup_session(session)
        
        return True
    
    def disable_personalization(self) -> bool:
        """
        Disable personalization mode
        
        Returns:
            bool: Whether disabling was successful
        """
        session = self.get_current_session()
        if not session:
            return False
        
        session.personalization_active = False
        session.updated_at = datetime.now().isoformat()
        self._backup_session(session)
        
        return True
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get session summary
        
        Returns:
            dict: Session summary information
        """
        session = self.get_current_session()
        if not session:
            return {"error": "No active session"}
        
        return session.get_session_summary()
    
    def reset_session(self) -> bool:
        """
        Reset current session
        
        Returns:
            bool: Whether reset was successful
        """
        try:
            # Get current case name
            current_case = st.session_state.get('case_name', 'madoff')
            current_user = st.session_state.get('user_id')
            
            # Clear session state
            for key in list(st.session_state.keys()):
                if key.startswith('cognitive_blackbox') or key in ['current_step', 'current_role', 'case_name', 'user_id']:
                    del st.session_state[key]
            
            # Reinitialize
            return self.initialize_session(current_case, current_user)
            
        except Exception as e:
            st.error(f"Session reset failed: {str(e)}")
            return False
    
    def export_session_data(self) -> Optional[str]:
        """
        Export session data as JSON
        
        Returns:
            str: JSON formatted session data, None if failed
        """
        session = self.get_current_session()
        if not session:
            return None
        
        try:
            session_dict = session.to_dict()
            return json.dumps(session_dict, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Session export failed: {str(e)}")
            return None
    
    def get_conversation_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get conversation history
        
        Args:
            limit: Maximum number of turns to return
        
        Returns:
            list: Conversation history
        """
        session = self.get_current_session()
        if not session:
            return []
        
        history = [turn.to_dict() for turn in session.conversation_history]
        
        if limit:
            return history[-limit:]
        
        return history
    
    def _generate_user_id(self) -> str:
        """Generate unique user ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"user_{timestamp}"
    
    def _backup_session(self, session: CaseSession) -> None:
        """
        Backup session
        
        Args:
            session: Session to backup
        """
        try:
            # Get existing backups
            backups = st.session_state.get(self.backup_key, [])
            
            # Add new backup
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'session_data': session.to_dict()
            }
            
            backups.append(backup_data)
            
            # Keep only recent backups
            if len(backups) > self.max_backup_count:
                backups = backups[-self.max_backup_count:]
            
            # Store backups
            st.session_state[self.backup_key] = backups
            
        except Exception as e:
            # Backup failure should not affect main functionality
            pass
    
    def get_session_metrics(self) -> Dict[str, Any]:
        """
        Get session performance metrics
        
        Returns:
            dict: Performance metrics
        """
        session = self.get_current_session()
        if not session:
            return {}
        
        metrics = session.performance_metrics
        
        return {
            'total_duration': metrics.calculate_total_duration(),
            'completion_rate': metrics.calculate_completion_rate(session.current_step),
            'api_calls': metrics.api_call_count,
            'total_tokens': metrics.total_tokens,
            'error_count': metrics.error_count,
            'step_durations': metrics.step_durations
        }

# Global instance
session_manager = SessionManager()
