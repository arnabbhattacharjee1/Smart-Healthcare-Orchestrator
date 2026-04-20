from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class Message:
    """Standardized communication message between agents."""
    def __init__(self, sender: str, receiver: str, content: Any, metadata: Optional[Dict] = None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.metadata = metadata or {}

    def __str__(self):
        return f"[{self.sender} -> {self.receiver}]: {self.content}"


class Agent(ABC):
    """Base class defining the Agent interface in ADK."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, message: Message) -> Message:
        """Process an incoming message and return an outgoing message."""
        pass


class Orchestrator(Agent):
    """A Primary Agent that manages coordination and state between sub-agents."""
    
    def __init__(self, name: str = "Orchestrator"):
        super().__init__(name, "Primary coordinator of specialized agents.")
        self.agents: Dict[str, Agent] = {}
        
    def register_agent(self, agent: Agent):
        """Register a sub-agent with the orchestrator."""
        self.agents[agent.name] = agent
        
    def route_message(self, target_agent_name: str, message: Message) -> Message:
        """Send a message to a specific agent and wait for a response."""
        if target_agent_name not in self.agents:
            raise ValueError(f"Agent '{target_agent_name}' not registered.")
        
        agent = self.agents[target_agent_name]
        print(f"[ADK Orbit] Routing to {agent.name}...")
        return agent.execute(message)

    @abstractmethod
    def run_plan(self, initial_input: Any) -> Any:
        """Define the orchestration plan/flow in derived classes."""
        pass

    def execute(self, message: Message) -> Message:
        # The orchestrator uses run_plan rather than a standard execute, 
        # but implements this to fulfill the base interface.
        result = self.run_plan(message.content)
        return Message(sender=self.name, receiver=message.sender, content=result)
