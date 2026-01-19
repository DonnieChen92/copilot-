"""
Model Orchestration Service
Coordinates requests across multiple AI models
"""
from typing import Dict, Any, Optional
from ..models.base import BaseModel, ModelProvider
from ..models.anthropic_model import ClaudeModel
from ..models.google_model import GeminiModel
from ..core.mcp import MCPProtocol
from ..core.security import ZeroTrustSecurity, AccessLevel


class ModelOrchestrator:
    """Orchestrates AI model interactions"""
    
    def __init__(self):
        self.models: Dict[ModelProvider, BaseModel] = {}
        self.mcp = MCPProtocol()
        self.security = ZeroTrustSecurity()
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize available models"""
        # These would be initialized with actual API keys from config
        self.models[ModelProvider.ANTHROPIC] = ClaudeModel()
        self.models[ModelProvider.GOOGLE] = GeminiModel()
    
    async def process_request(
        self,
        prompt: str,
        provider: ModelProvider,
        conversation_id: str,
        user_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Process a request through the specified model"""
        
        # Security check
        security_context = self.security.create_context(user_id)
        if not self.security.validate_request(security_context, AccessLevel.AUTHENTICATED):
            return {"error": "Unauthorized", "status": 401}
        
        # Get or create context
        context = self.mcp.get_context(conversation_id)
        if not context:
            context = self.mcp.create_context(conversation_id)
        
        # Get model
        model = self.models.get(provider)
        if not model:
            return {"error": f"Provider {provider.value} not available", "status": 404}
        
        # Generate response
        response = await model.generate(prompt, **kwargs)
        
        # Update context
        self.mcp.update_context(conversation_id, {
            "last_prompt": prompt,
            "last_response": response,
            "provider": provider.value
        })
        
        return response
    
    def get_available_providers(self) -> list:
        """Get list of available model providers"""
        return [provider.value for provider in self.models.keys()]
