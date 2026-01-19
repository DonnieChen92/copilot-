# API Documentation

## Base URL

```
Production: https://api.worldtree.ai
Development: http://localhost:8000
```

## Authentication

All API requests (except health checks) require authentication via Bearer token:

```bash
Authorization: Bearer <your_token>
```

## Endpoints

### Health Check

#### GET /
Get basic service status

**Response:**
```json
{
  "status": "healthy",
  "service": "Unified AI Matrix & WorldTree",
  "version": "0.1.0"
}
```

#### GET /health
Get detailed health status

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "api": "operational",
    "models": "operational",
    "database": "connected"
  }
}
```

### Model Operations

#### POST /api/v1/generate
Generate text using specified model

**Request:**
```json
{
  "prompt": "Explain quantum computing",
  "provider": "anthropic",
  "model_id": "claude-3-5-sonnet-20241022",
  "conversation_id": "conv-123",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

**Response:**
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "provider": "anthropic",
  "response": "Quantum computing is...",
  "metadata": {
    "tokens_used": 150,
    "latency_ms": 450
  }
}
```

#### POST /api/v1/stream
Stream text generation

**Request:** Same as /generate

**Response:** Server-Sent Events (SSE) stream

#### GET /api/v1/providers
List available model providers

**Response:**
```json
{
  "providers": [
    {
      "name": "anthropic",
      "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
      "capabilities": ["text_generation", "reasoning"]
    },
    {
      "name": "google",
      "models": ["gemini-2.0-flash", "gemini-pro"],
      "capabilities": ["text_generation", "image_generation", "reasoning"]
    }
  ]
}
```

### Context Management

#### GET /api/v1/context/{conversation_id}
Get conversation context

**Response:**
```json
{
  "conversation_id": "conv-123",
  "session_data": {
    "last_prompt": "...",
    "last_response": "...",
    "provider": "anthropic"
  },
  "metadata": {
    "created_at": "2026-01-14T10:00:00Z",
    "message_count": 5
  }
}
```

#### DELETE /api/v1/context/{conversation_id}
Clear conversation context

**Response:**
```json
{
  "status": "deleted",
  "conversation_id": "conv-123"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "details": "Missing required field: prompt"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "details": "Invalid or missing authentication token"
}
```

### 404 Not Found
```json
{
  "error": "Not found",
  "details": "Provider 'unknown' not available"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "details": "Failed to process request"
}
```

## Rate Limits

- 100 requests per minute per API key
- 10 concurrent streaming connections per API key

## SDK Examples

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/generate",
    headers={"Authorization": "Bearer YOUR_TOKEN"},
    json={
        "prompt": "What is machine learning?",
        "provider": "anthropic",
        "conversation_id": "conv-123"
    }
)
print(response.json())
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    prompt: 'What is machine learning?',
    provider: 'anthropic',
    conversation_id: 'conv-123'
  })
});
const data = await response.json();
console.log(data);
```
