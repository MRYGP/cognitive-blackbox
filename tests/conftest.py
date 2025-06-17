"""
Cognitive Black Box - Pytest Configuration
Shared test fixtures and configuration
"""

import pytest
import os
import sys
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, Generator
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import project modules
from utils.session_manager import SessionManager
from utils.ai_roles import AIRoleEngine
from utils.data_models import CaseSession, UserInput, ConversationTurn, CaseType
from config import ConfigManager

# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Configure pytest settings"""
    # Set test environment
    os.environ["APP_ENV"] = "test"
    os.environ["TEST_MODE"] = "true"
    os.environ["DEBUG_MODE"] = "false"
    
    # Mock API keys for testing
    os.environ["GEMINI_API_KEY"] = "test_gemini_key"
    os.environ["ANTHROPIC_API_KEY"] = "test_anthropic_key"

# =============================================================================
# SESSION FIXTURES
# =============================================================================

@pytest.fixture
def mock_session_manager() -> Generator[SessionManager, None, None]:
    """Create a mock session manager for testing"""
    session_manager = SessionManager()
    
    # Mock streamlit session state
    mock_session_state = MagicMock()
    mock_session_state.user_id = "test_user_123"
    mock_session_state.current_step = 1
    mock_session_state.case_name = "madoff"
    mock_session_state.current_role = "host"
    mock_session_state.conversation_history = []
    mock_session_state.user_inputs = {}
    mock_session_state.personalization_active = False
    
    # Replace st.session_state with our mock
    import streamlit as st
    original_session_state = getattr(st, 'session_state', None)
    st.session_state = mock_session_state
    
    yield session_manager
    
    # Restore original session state
    if original_session_state:
        st.session_state = original_session_state

@pytest.fixture
def sample_case_session() -> CaseSession:
    """Create a sample case session for testing"""
    return CaseSession(
        user_id="test_user_123",
        case_name="madoff",
        current_step=1,
        current_role="host"
    )

@pytest.fixture
def sample_user_input() -> UserInput:
    """Create a sample user input for testing"""
    return UserInput(
        input_type="company_name",
        content="Test Company Ltd"
    )

@pytest.fixture
def sample_conversation_turn() -> ConversationTurn:
    """Create a sample conversation turn for testing"""
    return ConversationTurn(
        role="host",
        message="Welcome to the cognitive experience",
        step=1
    )

# =============================================================================
# AI ENGINE FIXTURES
# =============================================================================

@pytest.fixture
def mock_ai_engine() -> Generator[AIRoleEngine, None, None]:
    """Create a mock AI engine for testing"""
    ai_engine = AIRoleEngine()
    
    # Mock API clients
    ai_engine.gemini_client = Mock()
    ai_engine.claude_client = Mock()
    
    # Mock API responses
    mock_response = Mock()
    mock_response.text = "This is a test AI response"
    ai_engine.gemini_client.generate_content.return_value = mock_response
    
    mock_claude_response = Mock()
    mock_claude_response.content = [Mock(text="This is a test Claude response")]
    ai_engine.claude_client.messages.create.return_value = mock_claude_response
    
    yield ai_engine

@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """Sample API response data"""
    return {
        "success": True,
        "content": "This is a test response from the AI",
        "token_count": 150,
        "response_time": 1.5
    }

# =============================================================================
# CONFIGURATION FIXTURES
# =============================================================================

@pytest.fixture
def test_config() -> ConfigManager:
    """Create test configuration"""
    # Set test environment variables
    test_env_vars = {
        "APP_ENV": "test",
        "DEBUG_MODE": "false",
        "ENABLE_CACHE": "false",
        "MOCK_API_RESPONSES": "true",
        "TEST_MODE": "true"
    }
    
    # Apply test environment variables
    for key, value in test_env_vars.items():
        os.environ[key] = value
    
    # Create and return test config
    config = ConfigManager()
    return config

@pytest.fixture
def mock_streamlit():
    """Mock streamlit components for testing"""
    mock_st = Mock()
    
    # Mock common streamlit functions
    mock_st.session_state = Mock()
    mock_st.error = Mock()
    mock_st.success = Mock()
    mock_st.info = Mock()
    mock_st.warning = Mock()
    mock_st.write = Mock()
    mock_st.markdown = Mock()
    mock_st.button = Mock(return_value=False)
    mock_st.text_input = Mock(return_value="")
    mock_st.selectbox = Mock(return_value="option1")
    mock_st.checkbox = Mock(return_value=False)
    
    return mock_st

# =============================================================================
# DATA FIXTURES
# =============================================================================

@pytest.fixture
def sample_conversation_history() -> list:
    """Sample conversation history for testing"""
    return [
        ConversationTurn(
            role="host",
            message="Welcome to the experience",
            step=1
        ),
        ConversationTurn(
            role="host", 
            message="Let's begin with your background",
            step=1
        ),
        ConversationTurn(
            role="investor",
            message="Now let's look at the reality",
            step=2
        )
    ]

@pytest.fixture
def sample_user_inputs() -> Dict[str, UserInput]:
    """Sample user inputs for testing"""
    return {
        "company_name": UserInput(
            input_type="company_name",
            content="Test Tech Company"
        ),
        "investment_amount": UserInput(
            input_type="investment_amount", 
            content="5000万"
        ),
        "decision_context": UserInput(
            input_type="decision_context",
            content="Looking for stable investment opportunities"
        )
    }

@pytest.fixture
def sample_magic_moments() -> list:
    """Sample magic moments for testing"""
    from utils.data_models import MagicMoment
    return [
        MagicMoment(
            name="reality_shock",
            trigger_step=2,
            description="Reality disruption moment"
        ),
        MagicMoment(
            name="framework_insight",
            trigger_step=3,
            description="Framework understanding moment"
        )
    ]

# =============================================================================
# UTILITY FIXTURES
# =============================================================================

@pytest.fixture
def temp_file(tmp_path) -> Generator[Path, None, None]:
    """Create a temporary file for testing"""
    file_path = tmp_path / "test_file.json"
    file_path.write_text('{"test": "data"}')
    yield file_path

@pytest.fixture
def mock_datetime():
    """Mock datetime for consistent testing"""
    from unittest.mock import patch
    import datetime
    
    fixed_datetime = datetime.datetime(2024, 12, 19, 12, 0, 0)
    
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value = fixed_datetime
        mock_dt.fromisoformat.side_effect = datetime.datetime.fromisoformat
        yield mock_dt

# =============================================================================
# PARAMETRIZED FIXTURES
# =============================================================================

@pytest.fixture(params=["madoff", "ltcm", "lehman"])
def case_type(request) -> str:
    """Parametrized fixture for different case types"""
    return request.param

@pytest.fixture(params=["host", "investor", "mentor", "assistant"])
def role_type(request) -> str:
    """Parametrized fixture for different role types"""
    return request.param

@pytest.fixture(params=[1, 2, 3, 4])
def step_number(request) -> int:
    """Parametrized fixture for different step numbers"""
    return request.param

# =============================================================================
# CLEANUP FIXTURES
# =============================================================================

@pytest.fixture(autouse=True)
def cleanup_environment():
    """Automatically cleanup environment after each test"""
    yield
    
    # Clean up any test-specific environment variables
    test_vars = [
        "TEST_USER_ID",
        "TEST_CASE_NAME", 
        "TEST_CURRENT_STEP"
    ]
    
    for var in test_vars:
        if var in os.environ:
            del os.environ[var]

@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests"""
    # Clear any cached instances or global state
    yield
    
    # Reset any global state if needed
    # This ensures test isolation

# =============================================================================
# PERFORMANCE FIXTURES
# =============================================================================

@pytest.fixture
def performance_timer():
    """Timer fixture for performance testing"""
    import time
    
    start_time = time.time()
    
    def get_elapsed():
        return time.time() - start_time
    
    return get_elapsed

# =============================================================================
# ERROR TESTING FIXTURES
# =============================================================================

@pytest.fixture
def api_error_scenarios():
    """Different API error scenarios for testing"""
    return {
        "timeout": Exception("Request timeout"),
        "rate_limit": Exception("Rate limit exceeded"),
        "invalid_key": Exception("Invalid API key"),
        "server_error": Exception("Internal server error"),
        "network_error": Exception("Network connection failed")
    }

# =============================================================================
# MARKERS
# =============================================================================

def pytest_configure(config):
    """Register custom pytest markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests that require API access"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
