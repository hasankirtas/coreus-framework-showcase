from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..typing.models import AgentInput, AgentOutput

class BaseAgent(ABC):
    """
    Abstract base class for all autonomous agents in the Coreus system.
    Enforces a strict contract for inputs, outputs, and lifecycle management.
    """

    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self._initialized = False

    async def start(self) -> None:
        """Initialize agent resources (DB connections, model loaders)."""
        if not self._initialized:
            await self.initialize()
            self._initialized = True

    @abstractmethod
    async def initialize(self) -> None:
        """User-defined initialization logic."""
        pass

    async def process(self, input_data: AgentInput) -> AgentOutput:
        """
        Main execution entry point.
        
        In the full framework, this method wraps execution with:
        1. Context Injection (Memory)
        2. Distributed Tracing (Observability)
        3. Error Recovery Strategies
        """
        if not self._initialized:
            await self.start()
            
        # [Trace Start Point]
        try:
            # Core logic execution
            result = await self._run(input_data)
            return result
        except Exception as e:
            # [Error Handler Hook]
            # Returns standardized error envelope
            raise e 
            
    @abstractmethod
    async def _run(self, input_data: AgentInput) -> AgentOutput:
        """Core business logic implementation."""
        pass

    async def stop(self) -> None:
        """Cleanup resources."""
        await self.cleanup()

    @abstractmethod
    async def cleanup(self) -> None:
        """User-defined cleanup logic."""
        pass
