"""
Cognitive Black Box - Data Models Definition
Define all data structures used in the system
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime

class CaseType(Enum):
    """Case type enumeration"""
    MADOFF = "madoff"           # Madoff case - Halo effect
    LTCM = "ltcm"              # Long-Term Capital Management - Overconfidence
    LEHMAN = "lehman"          # Lehman Brothers - Confirmation bias

class RoleType(Enum):
    """Role type enumeration"""
    HOST = "host"              # Host - Guidance and immersion
    INVESTOR = "investor"      # Investor - Reality disruption
    MENTOR = "mentor"          # Mentor - Framework reconstruction
    ASSISTANT = "assistant"    # Assistant - Capability armament

class StepStatus(Enum):
    """Step status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class UserInput:
    """User input data structure"""
    input_type: str                    # Input type (company_name, investment_amount, etc.)
    content: str                       # Input content
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    validation_status: bool = True     # Validation status
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'input_type': self.input_type,
            'content': self.content,
            'timestamp': self.timestamp,
            'validation_status': self.validation_status,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserInput':
        """Create instance from dictionary"""
        return cls(
            input_type=data['input_type'],
            content=data['content'],
            timestamp=data.get('timestamp', datetime.now().isoformat()),
            validation_status=data.get('validation_status', True),
            metadata=data.get('metadata', {})
        )

@dataclass
class ConversationTurn:
    """Conversation turn data structure"""
    role: str                          # Role name
    message: str                       # Message content
    step: int                          # Belonging step
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    user_input: Optional[UserInput] = None  # Associated user input
    response_time: float = 0.0         # Response time (seconds)
    api_used: str = ""                 # API used
    token_count: int = 0               # Token usage
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'role': self.role,
            'message': self.message,
            'step': self.step,
            'timestamp': self.timestamp,
            'user_input': self.user_input.to_dict() if self.user_input else None,
            'response_time': self.response_time,
            'api_used': self.api_used,
            'token_count': self.token_count,
            'metadata': self.metadata
        }

@dataclass
class MagicMoment:
    """Magic moment data structure"""
    name: str                          # Moment name
    trigger_step: int                  # Trigger step
    description: str                   # Description
    triggered: bool = False            # Whether triggered
    trigger_time: Optional[str] = None # Trigger time
    effect_config: Dict[str, Any] = field(default_factory=dict)  # Effect configuration
    
    def trigger(self) -> None:
        """Trigger magic moment"""
        self.triggered = True
        self.trigger_time = datetime.now().isoformat()

@dataclass 
class DecisionTool:
    """Decision tool data structure"""
    tool_name: str                     # Tool name
    tool_type: str                     # Tool type (framework, checklist, etc.)
    content: Dict[str, Any]            # Tool content
    personalized: bool = False         # Whether personalized
    generation_time: str = field(default_factory=lambda: datetime.now().isoformat())
    usage_count: int = 0               # Usage count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'tool_name': self.tool_name,
            'tool_type': self.tool_type,
            'content': self.content,
            'personalized': self.personalized,
            'generation_time': self.generation_time,
            'usage_count': self.usage_count
        }

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    session_start: str = field(default_factory=lambda: datetime.now().isoformat())
    session_end: Optional[str] = None
    total_duration: float = 0.0        # Total duration (seconds)
    step_durations: Dict[int, float] = field(default_factory=dict)  # Step durations
    api_call_count: int = 0            # API call count
    total_tokens: int = 0              # Total token usage
    user_engagement_score: float = 0.0 # User engagement score
    completion_rate: float = 0.0       # Completion rate
    error_count: int = 0               # Error count
    
    def calculate_total_duration(self) -> float:
        """Calculate total duration"""
        if self.session_end:
            start = datetime.fromisoformat(self.session_start)
            end = datetime.fromisoformat(self.session_end)
            self.total_duration = (end - start).total_seconds()
        return self.total_duration
    
    def calculate_completion_rate(self, current_step: int, total_steps: int = 4) -> float:
        """Calculate completion rate"""
        self.completion_rate = (current_step - 1) / total_steps * 100
        return self.completion_rate

@dataclass
class CaseSession:
    """Complete session data structure"""
    user_id: str
    case_name: str
    current_step: int = 1
    current_role: str = "host"
    status: StepStatus = StepStatus.NOT_STARTED
    
    # Core data
    conversation_history: List[ConversationTurn] = field(default_factory=list)
    user_inputs: Dict[str, UserInput] = field(default_factory=dict)
    magic_moments: List[MagicMoment] = field(default_factory=list)
    generated_tools: List[DecisionTool] = field(default_factory=list)
    
    # Personalization related
    personalization_active: bool = False
    original_case_data: Dict[str, Any] = field(default_factory=dict)
    
    # Performance and error tracking
    performance_metrics: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    error_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_conversation_turn(self, turn: ConversationTurn) -> None:
        """Add conversation turn"""
        self.conversation_history.append(turn)
        self.updated_at = datetime.now().isoformat()
        
        # Update performance metrics
        self.performance_metrics.api_call_count += 1
        self.performance_metrics.total_tokens += turn.token_count
    
    def add_user_input(self, input_data: UserInput) -> None:
        """Add user input"""
        self.user_inputs[input_data.input_type] = input_data
        self.updated_at = datetime.now().isoformat()
    
    def trigger_magic_moment(self, moment_name: str) -> bool:
        """Trigger magic moment"""
        for moment in self.magic_moments:
            if moment.name == moment_name and not moment.triggered:
                moment.trigger()
                self.updated_at = datetime.now().isoformat()
                return True
        return False
    
    def add_generated_tool(self, tool: DecisionTool) -> None:
        """Add generated tool"""
        self.generated_tools.append(tool)
        self.updated_at = datetime.now().isoformat()
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get current context"""
        return {
            'user_id': self.user_id,
            'case_name': self.case_name,
            'current_step': self.current_step,
            'current_role': self.current_role,
            'personalization_active': self.personalization_active,
            'user_inputs': {k: v.to_dict() for k, v in self.user_inputs.items()},
            'conversation_count': len(self.conversation_history),
            'magic_moments_triggered': [m.name for m in self.magic_moments if m.triggered],
            'tools_generated': len(self.generated_tools)
        }
    
    def advance_step(self) -> bool:
        """Advance to next step"""
        if self.current_step < 4:
            # Record current step end time
            if self.current_step in self.performance_metrics.step_durations:
                step_start = self.performance_metrics.step_durations[self.current_step]
                current_time = datetime.now().timestamp()
                duration = current_time - step_start
                self.performance_metrics.step_durations[self.current_step] = duration
            
            self.current_step += 1
            
            # Update role
            role_map = {1: "host", 2: "investor", 3: "mentor", 4: "assistant"}
            self.current_role = role_map.get(self.current_step, "host")
            
            # Record new step start time
            self.performance_metrics.step_durations[self.current_step] = datetime.now().timestamp()
            
            self.updated_at = datetime.now().isoformat()
            return True
        
        return False
    
    def log_error(self, error_message: str, error_type: str = "general") -> None:
        """Log error"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message,
            'step': self.current_step,
            'role': self.current_role
        }
        
        self.error_history.append(error_entry)
        self.performance_metrics.error_count += 1
        self.updated_at = datetime.now().isoformat()
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get session summary"""
        return {
            'user_id': self.user_id,
            'case_name': self.case_name,
            'current_progress': f"{self.current_step}/4",
            'total_duration': self.performance_metrics.calculate_total_duration(),
            'completion_rate': self.performance_metrics.calculate_completion_rate(self.current_step),
            'conversation_turns': len(self.conversation_history),
            'personalization_used': self.personalization_active,
            'tools_generated': len(self.generated_tools),
            'api_calls': self.performance_metrics.api_call_count,
            'errors': self.performance_metrics.error_count,
            'magic_moments': len([m for m in self.magic_moments if m.triggered])
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'user_id': self.user_id,
            'case_name': self.case_name,
            'current_step': self.current_step,
            'current_role': self.current_role,
            'status': self.status.value,
            'conversation_history': [turn.to_dict() for turn in self.conversation_history],
            'user_inputs': {k: v.to_dict() for k, v in self.user_inputs.items()},
            'personalization_active': self.personalization_active,
            'original_case_data': self.original_case_data,
            'generated_tools': [tool.to_dict() for tool in self.generated_tools],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Predefined case configurations
CASE_CONFIGS = {
    CaseType.MADOFF: {
        'name': 'Madoff Ponzi Scheme',
        'cognitive_bias': 'Halo Effect',
        'description': 'The fatal halo of former NASDAQ chairman',
        'default_inputs': {
            'company_name': 'CEO Li Tech Company',
            'investment_amount': '50 million RMB',
            'decision_context': 'Seeking stable investment opportunities for company'
        },
        'magic_moments': [
            MagicMoment(
                name="reality_disruption",
                trigger_step=2,
                description="Cognitive shock moment when switching from host to investor",
                effect_config={
                    'audio': 'warning_sound.mp3',
                    'visual': 'red_alert_animation',
                    'duration': 3.0
                }
            )
        ]
    },
    
    CaseType.LTCM: {
        'name': 'Long-Term Capital Management',
        'cognitive_bias': 'Overconfidence',
        'description': 'The downfall of the Nobel Prize winning team',
        'default_inputs': {
            'company_name': 'Quantitative Fund',
            'team_background': 'Technical analysis team', 
            'decision_context': 'Evaluating quantitative strategy investment'
        },
        'magic_moments': [
            MagicMoment(
                name="model_failure",
                trigger_step=2,
                description="Fragility of complex models in reality",
                effect_config={
                    'visual': 'model_breakdown_animation',
                    'duration': 4.0
                }
            )
        ]
    },
    
    CaseType.LEHMAN: {
        'name': 'Lehman Brothers',
        'cognitive_bias': 'Confirmation Bias',
        'description': 'The obsession that housing prices will never fall',
        'default_inputs': {
            'company_name': 'Real Estate Enterprise',
            'industry_experience': '15 years',
            'decision_context': 'Judging real estate market cycle'
        },
        'magic_moments': [
            MagicMoment(
                name="trend_reversal",
                trigger_step=2,
                description="Sudden reversal of seemingly eternal trend",
                effect_config={
                    'visual': 'trend_reversal_chart',
                    'duration': 5.0
                }
            )
        ]
    }
}

# Utility functions
def create_case_session(user_id: str, case_type: CaseType) -> CaseSession:
    """Create new case session"""
    case_config = CASE_CONFIGS[case_type]
    
    session = CaseSession(
        user_id=user_id,
        case_name=case_type.value
    )
    
    # Add case-specific magic moments
    session.magic_moments = case_config['magic_moments'].copy()
    
    # Set default case data
    session.original_case_data = case_config['default_inputs'].copy()
    
    return session

def get_case_info(case_type: CaseType) -> Dict[str, Any]:
    """Get case information"""
    return CASE_CONFIGS.get(case_type, {})

def validate_user_input(input_data: UserInput) -> bool:
    """Validate user input"""
    if not input_data.content or not input_data.content.strip():
        return False
    
    # Can add more validation logic based on input_type
    return True
