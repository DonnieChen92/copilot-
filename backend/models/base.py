"""
Base Model Interface
Common interface for all AI model providers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum


class ModelProvider(Enum):
    """Supported AI model providers"""
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    OPENAI = "openai"


class ModelCapability(Enum):
    """Model capabilities"""
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    VIDEO_GENERATION = "video_generation"
    EMBEDDING = "embedding"
    REASONING = "reasoning"


class BaseModel(ABC):
    """Base class for all AI model integrations"""
    
    def __init__(self, model_id: str, provider: ModelProvider):
        self.model_id = model_id
        self.provider = provider
        self.capabilities: List[ModelCapability] = []
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response from the model"""
        pass
    
    @abstractmethod
    async def stream_generate(self, prompt: str, **kwargs):
        """Stream response from the model"""
        pass
    
    def get_capabilities(self) -> List[ModelCapability]:
        """Get model capabilities"""
        return self.capabilities
    
    def supports_capability(self, capability: ModelCapability) -> bool:
        """Check if model supports a capability"""
        return capability in self.capabilities
