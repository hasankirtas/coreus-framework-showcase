from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ConfigDict

class AgentInput(BaseModel):
    """
    Standardized input contract for all agents.
    Ensures type safety across the distributed system.
    """
    query: str = Field(..., description="The main instruction or question to process")
    user_id: Optional[str] = Field(None, description="Unique identifier for context isolation")
    session_id: Optional[str] = Field(None, description="Tracking ID for the current workflow session")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context or config parameters")
    
    model_config = ConfigDict(extra="allow")

class AgentOutput(BaseModel):
    """
    Standardized output contract.
    Guaranteeing consistent response structure.
    """
    content: Any = Field(..., description="The primary result payload")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    latency_ms: Optional[float] = Field(None, description="Execution time in milliseconds")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(extra="allow")

class WorkflowState(BaseModel):
    """
    Shared state object for the orchestration engine.
    Passed between agents during graph execution.
    """
    current_step: str
    history: List[Dict[str, Any]] = Field(default_factory=list)
    context_variables: Dict[str, Any] = Field(default_factory=dict)
    is_complete: bool = False
