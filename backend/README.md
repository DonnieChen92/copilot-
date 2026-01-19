# Backend - Unified AI Matrix & WorldTree

Backend services for the Unified AI Matrix & WorldTree platform.

## Structure

- `api/` - FastAPI REST API endpoints
- `models/` - AI model integration and wrappers
- `services/` - Business logic and orchestration services
- `core/` - Core utilities and shared components

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn api.main:app --reload
```

## Environment Variables

Create a `.env` file with the following:

```
# API Keys
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
AZURE_API_KEY=your_key_here

# Configuration
ENVIRONMENT=development
LOG_LEVEL=info
```
