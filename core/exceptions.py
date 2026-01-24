class CoreusError(Exception):
    """Base exception for all Coreus framework errors."""
    pass

class ValidationContractError(CoreusError):
    """Raised when data violates the strict schema contracts (AgentInput/AgentOutput)."""
    pass

class OrchestrationTraverseError(CoreusError):
    """Raised when the workflow graph reaches an invalid or cyclic state."""
    pass

class StorageConnectionError(CoreusError):
    """Raised when the persistence layer (Memory/Vector Store) is unreachable."""
    pass

class ServiceAvailabilityError(CoreusError):
    """Raised when external services trigger safety guards (Circuit Breakers)."""
    pass

class AgentLifecycleError(CoreusError):
    """Raised when an agent fails to initialize or cleanup resources correctly."""
    pass
