"""
Model Context Protocol (MCP) Implementation
Standardized context sharing across different AI models
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel


class ModelContext(BaseModel):
    """Context shared between models"""
    conversation_id: str
    session_data: Dict[str, Any]
    metadata: Dict[str, Any] = {}


class MCPProtocol:
    """Model Context Protocol implementation"""
    
    def __init__(self):
        self.contexts: Dict[str, ModelContext] = {}
    
    def create_context(self, conversation_id: str) -> ModelContext:
        """Create a new context for a conversation"""
        context = ModelContext(
            conversation_id=conversation_id,
            session_data={},
            metadata={}
        )
        self.contexts[conversation_id] = context
        return context
    
    def get_context(self, conversation_id: str) -> Optional[ModelContext]:
        """Retrieve context for a conversation"""
        return self.contexts.get(conversation_id)
    
    def update_context(self, conversation_id: str, data: Dict[str, Any]) -> None:
        """Update context with new data"""
        if conversation_id in self.contexts:
            self.contexts[conversation_id].session_data.update(data)
    
    def clear_context(self, conversation_id: str) -> None:
        """Clear context for a conversation"""
        if conversation_id in self.contexts:
            del self.contexts[conversation_id]
