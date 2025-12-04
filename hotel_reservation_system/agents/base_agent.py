"""Base agent implementation"""

from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel
from datetime import datetime


class MessageType(str, Enum):
    """Types of messages agents can exchange"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


class AgentMessage(BaseModel):
    """Message structure for agent communication"""
    message_id: str
    sender: str
    receiver: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime = datetime.now()
    reply_to: Optional[str] = None


class BaseAgent:
    """Base class for all agents in the system"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.message_queue = []
        
    def send_message(self, receiver: str, message_type: MessageType, 
                    content: Dict[str, Any], reply_to: Optional[str] = None) -> AgentMessage:
        """Create and send a message to another agent"""
        message = AgentMessage(
            message_id=f"{self.agent_id}-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            content=content,
            reply_to=reply_to
        )
        return message
    
    def receive_message(self, message: AgentMessage):
        """Receive a message from another agent"""
        self.message_queue.append(message)
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a received message - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process_message")
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.agent_id}, name={self.name})"
