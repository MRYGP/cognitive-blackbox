"""
Cognitive Black Box - Error Handling System
Provides comprehensive error handling and graceful degradation
"""

import streamlit as st
import logging
import traceback
import time
from typing import Dict, Any, Optional, Callable, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import functools

class ErrorType(Enum):
    """Error type enumeration"""
    API_ERROR = "api_error"
    VALIDATION_ERROR = "validation_error"
    SESSION_ERROR = "session_error"
    CONFIGURATION_ERROR = "config_error"
    SYSTEM_ERROR = "system_error"
    USER_INPUT_ERROR = "user_input_error"
    NETWORK_ERROR = "network_error"

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ErrorInfo:
    """Error information structure"""
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    user_message: str
    timestamp: str
    context: Dict[str, Any]
    traceback_info: Optional[str] = None
    suggested_action: Optional[str] = None

class ErrorHandler:
    """
    Comprehensive error handling system with graceful degradation
    """
    
    def __init__(self):
        """Initialize error handler"""
        self._setup_logging()
        self.error_history = []
        self.max_error_history = 100
        
        # Error message templates
        self.user_messages = {
            ErrorType.API_ERROR: "AI服务暂时不可用，我们正在使用备用方案为您服务。",
            ErrorType.VALIDATION_ERROR: "输入格式不正确，请检查并重新输入。",
            ErrorType.SESSION_ERROR: "会话出现问题，正在尝试恢复您的进度。",
            ErrorType.CONFIGURATION_ERROR: "系统配置错误，请稍后重试。",
            ErrorType.SYSTEM_ERROR: "系统出现临时问题，正在自动修复。",
            ErrorType.USER_INPUT_ERROR: "请检查您的输入内容。",
            ErrorType.NETWORK_ERROR: "网络连接不稳定，请稍后重试。"
        }
        
        # Recovery strategies
        self.recovery_strategies = {
            ErrorType.API_ERROR: self._recover_api_error,
            ErrorType.SESSION_ERROR: self._recover_session_error,
            ErrorType.CONFIGURATION_ERROR: self._recover_config_error,
            ErrorType.VALIDATION_ERROR: self._recover_validation_error
        }
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, 
                    exception: Exception, 
                    error_type: ErrorType,
                    context: Dict[str, Any] = None,
                    user_visible: bool = True,
                    auto_recover: bool = True) -> ErrorInfo:
        """
        Handle error with comprehensive logging and recovery
        
        Args:
            exception: The exception that occurred
            error_type: Type of error
            context: Additional context information
            user_visible: Whether to show error to user
            auto_recover: Whether to attempt automatic recovery
        
        Returns:
            ErrorInfo: Comprehensive error information
        """
        try:
            # Determine severity
            severity = self._determine_severity(error_type, exception)
            
            # Create error info
            error_info = ErrorInfo(
                error_type=error_type,
                severity=severity,
                message=str(exception),
                user_message=self._get_user_message(error_type, exception),
                timestamp=datetime.now().isoformat(),
                context=context or {},
                traceback_info=traceback.format_exc(),
                suggested_action=self._get_suggested_action(error_type)
            )
            
            # Log error
            self._log_error(error_info)
            
            # Store in history
            self._store_error(error_info)
            
            # Show to user if needed
            if user_visible:
                self._display_user_error(error_info)
            
            # Attempt recovery
            if auto_recover:
                self._attempt_recovery(error_info)
            
            return error_info
            
        except Exception as e:
            # Critical error in error handler itself
            self.logger.critical(f"Error handler failed: {str(e)}")
            self._display_critical_error()
            return self._create_fallback_error_info(exception)
    
    def handle_api_timeout(self, api_name: str, timeout_duration: float) -> None:
        """Handle API timeout specifically"""
        context = {
            'api_name': api_name,
            'timeout_duration': timeout_duration,
            'timestamp': time.time()
        }
        
        error_info = ErrorInfo(
            error_type=ErrorType.API_ERROR,
            severity=ErrorSeverity.MEDIUM,
            message=f"API timeout for {api_name} after {timeout_duration}s",
            user_message="AI响应时间较长，正在为您切换到更快的处理方式。",
            timestamp=datetime.now().isoformat(),
            context=context,
            suggested_action="use_fallback_response"
        )
        
        self._log_error(error_info)
        self._store_error(error_info)
        
        # Show timeout message to user
        with st.spinner("正在为您切换到更快的处理方式..."):
            time.sleep(1)  # Brief pause for user experience
        
        st.info("⚡ 我们已切换到快速模式，继续为您提供优质体验。")
    
    def handle_validation_error(self, field: str, value: str, error_message: str) -> None:
        """Handle validation error specifically"""
        context = {
            'field': field,
            'value': value[:100],  # Truncate for privacy
            'validation_error': error_message
        }
        
        error_info = ErrorInfo(
            error_type=ErrorType.VALIDATION_ERROR,
            severity=ErrorSeverity.LOW,
            message=f"Validation failed for {field}: {error_message}",
            user_message=f"请检查{field}的输入格式：{error_message}",
            timestamp=datetime.now().isoformat(),
            context=context,
            suggested_action="correct_input"
        )
        
        self._log_error(error_info)
        self._store_error(error_info)
        
        # Show specific validation error
        st.error(f"❌ {error_info.user_message}")
    
    def handle_session_error(self, operation: str, details: str = None) -> bool:
        """
        Handle session-related errors
        
        Args:
            operation: The operation that failed
            details: Additional error details
        
        Returns:
            bool: True if recovery was successful
        """
        context = {
            'operation': operation,
            'details': details,
            'session_state_keys': list(st.session_state.keys()) if hasattr(st, 'session_state') else []
        }
        
        error_info = ErrorInfo(
            error_type=ErrorType.SESSION_ERROR,
            severity=ErrorSeverity.HIGH,
            message=f"Session error during {operation}: {details}",
            user_message="会话出现问题，正在为您恢复...",
            timestamp=datetime.now().isoformat(),
            context=context,
            suggested_action="recover_session"
        )
        
        self._log_error(error_info)
        self._store_error(error_info)
        
        # Attempt session recovery
        return self._recover_session_error(error_info)
    
    def _determine_severity(self, error_type: ErrorType, exception: Exception) -> ErrorSeverity:
        """Determine error severity based on type and exception"""
        # Critical errors
        if "critical" in str(exception).lower():
            return ErrorSeverity.CRITICAL
        
        # High severity errors
        if error_type in [ErrorType.SESSION_ERROR, ErrorType.CONFIGURATION_ERROR]:
            return ErrorSeverity.HIGH
        
        # Medium severity errors
        if error_type in [ErrorType.API_ERROR, ErrorType.SYSTEM_ERROR]:
            return ErrorSeverity.MEDIUM
        
        # Low severity errors
        return ErrorSeverity.LOW
    
    def _get_user_message(self, error_type: ErrorType, exception: Exception) -> str:
        """Get user-friendly error message"""
        base_message = self.user_messages.get(error_type, "系统出现临时问题，请稍后重试。")
        
        # Customize message based on specific exception
        if "timeout" in str(exception).lower():
            return "响应时间较长，正在为您切换到快速模式。"
        elif "network" in str(exception).lower():
            return "网络连接不稳定，正在重新连接。"
        elif "authentication" in str(exception).lower():
            return "服务认证出现问题，正在自动修复。"
        
        return base_message
    
    def _get_suggested_action(self, error_type: ErrorType) -> str:
        """Get suggested action for error recovery"""
        action_map = {
            ErrorType.API_ERROR: "use_fallback_response",
            ErrorType.VALIDATION_ERROR: "correct_input",
            ErrorType.SESSION_ERROR: "recover_session",
            ErrorType.CONFIGURATION_ERROR: "reload_config",
            ErrorType.SYSTEM_ERROR: "restart_component",
            ErrorType.NETWORK_ERROR: "retry_connection"
        }
        return action_map.get(error_type, "manual_intervention")
    
    def _log_error(self, error_info: ErrorInfo) -> None:
        """Log error information"""
        log_message = f"{error_info.error_type.value} - {error_info.message}"
        
        if error_info.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message, extra={'error_info': error_info.__dict__})
        elif error_info.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message, extra={'error_info': error_info.__dict__})
        elif error_info.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message, extra={'error_info': error_info.__dict__})
        else:
            self.logger.info(log_message, extra={'error_info': error_info.__dict__})
    
    def _store_error(self, error_info: ErrorInfo) -> None:
        """Store error in history"""
        self.error_history.append(error_info)
        
        # Keep only recent errors
        if len(self.error_history) > self.max_error_history:
            self.error_history = self.error_history[-self.max_error_history:]
    
    def _display_user_error(self, error_info: ErrorInfo) -> None:
        """Display error to user"""
        if error_info.severity == ErrorSeverity.CRITICAL:
            st.error(f"🚨 严重错误：{error_info.user_message}")
        elif error_info.severity == ErrorSeverity.HIGH:
            st.error(f"❌ {error_info.user_message}")
        elif error_info.severity == ErrorSeverity.MEDIUM:
            st.warning(f"⚠️ {error_info.user_message}")
        else:
            st.info(f"ℹ️ {error_info.user_message}")
    
    def _display_critical_error(self) -> None:
        """Display critical system error"""
        st.error("🚨 系统遇到严重问题，请刷新页面重试。如果问题持续存在，请联系技术支持。")
        
        if st.button("🔄 刷新页面"):
            st.rerun()
    
    def _attempt_recovery(self, error_info: ErrorInfo) -> bool:
        """Attempt automatic error recovery"""
        recovery_func = self.recovery_strategies.get(error_info.error_type)
        
        if recovery_func:
            try:
                return recovery_func(error_info)
            except Exception as e:
                self.logger.error(f"Recovery failed for {error_info.error_type}: {str(e)}")
        
        return False
    
    def _recover_api_error(self, error_info: ErrorInfo) -> bool:
        """Recover from API errors"""
        # Use fallback responses
        context = error_info.context
        if 'role' in context:
            # Store fallback flag for AI engine
            if 'api_fallback_active' not in st.session_state:
                st.session_state.api_fallback_active = True
            return True
        
        return False
    
    def _recover_session_error(self, error_info: ErrorInfo) -> bool:
        """Recover from session errors"""
        try:
            # Try to reinitialize critical session variables
            if 'current_step' not in st.session_state:
                st.session_state.current_step = 1
            
            if 'case_name' not in st.session_state:
                st.session_state.case_name = 'madoff'
            
            if 'initialized' not in st.session_state:
                st.session_state.initialized = False
            
            st.info("✅ 会话已恢复，您可以继续体验。")
            return True
            
        except Exception as e:
            self.logger.error(f"Session recovery failed: {str(e)}")
            return False
    
    def _recover_config_error(self, error_info: ErrorInfo) -> bool:
        """Recover from configuration errors"""
        # Use default configurations
        st.warning("⚠️ 使用默认配置继续运行。")
        return True
    
    def _recover_validation_error(self, error_info: ErrorInfo) -> bool:
        """Recover from validation errors"""
        # Validation errors typically require user action
        return False
    
    def _create_fallback_error_info(self, exception: Exception) -> ErrorInfo:
        """Create fallback error info when error handler fails"""
        return ErrorInfo(
            error_type=ErrorType.SYSTEM_ERROR,
            severity=ErrorSeverity.CRITICAL,
            message=str(exception),
            user_message="系统遇到严重问题，请刷新页面重试。",
            timestamp=datetime.now().isoformat(),
            context={},
            suggested_action="manual_intervention"
        )
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        if not self.error_history:
            return {'total_errors': 0}
        
        stats = {
            'total_errors': len(self.error_history),
            'by_type': {},
            'by_severity': {},
            'recent_errors': len([e for e in self.error_history[-10:]]),
            'critical_errors': len([e for e in self.error_history if e.severity == ErrorSeverity.CRITICAL])
        }
        
        # Count by type
        for error in self.error_history:
            error_type = error.error_type.value
            stats['by_type'][error_type] = stats['by_type'].get(error_type, 0) + 1
            
            severity = error.severity.value
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
        
        return stats
    
    def clear_error_history(self) -> None:
        """Clear error history"""
        self.error_history.clear()
        self.logger.info("Error history cleared")

def error_handler_decorator(error_type: ErrorType = ErrorType.SYSTEM_ERROR, 
                          user_visible: bool = True,
                          auto_recover: bool = True):
    """
    Decorator for automatic error handling
    
    Args:
        error_type: Type of error to handle
        user_visible: Whether to show error to user
        auto_recover: Whether to attempt automatic recovery
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    'function_name': func.__name__,
                    'args': str(args)[:100],
                    'kwargs': str(kwargs)[:100]
                }
                
                error_handler.handle_error(
                    exception=e,
                    error_type=error_type,
                    context=context,
                    user_visible=user_visible,
                    auto_recover=auto_recover
                )
                
                # Return None or appropriate fallback value
                return None
        return wrapper
    return decorator

# Global error handler instance
error_handler = ErrorHandler()
