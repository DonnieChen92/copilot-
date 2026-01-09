"""FastAPI ML Model Serving Application."""
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .model_loader import BaseModelLoader, get_model_loader
from .monitoring import MetricsCollector, PredictionTimer, metrics_collector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global model registry
model_registry: Dict[str, BaseModelLoader] = {}


class PredictionRequest(BaseModel):
    """Request model for predictions."""
    model_name: str = Field(..., description="Name of the model to use")
    input_data: List[List[float]] = Field(..., description="Input data as 2D array")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "default",
                "input_data": [[1.0, 2.0, 3.0, 4.0]]
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    model_name: str
    predictions: List[Any]
    latency_ms: float
    timestamp: str


class ModelInfo(BaseModel):
    """Model information."""
    name: str
    format: str
    loaded: bool
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    models: Dict[str, Dict[str, Any]]
    uptime_seconds: float


def load_models_from_config() -> None:
    """Load models based on environment configuration."""
    model_path = os.getenv("MODEL_PATH", "")
    model_name = os.getenv("MODEL_NAME", "default")

    if model_path and os.path.exists(model_path):
        try:
            loader = get_model_loader(model_path)
            loader.load()
            model_registry[model_name] = loader
            metrics_collector.register_model(model_name)
            logger.info(f"Loaded model '{model_name}' from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {e}")
    else:
        logger.warning("No MODEL_PATH configured or path doesn't exist. "
                      "Use /models/load endpoint to load models.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting ML Model Serving Application...")
    load_models_from_config()
    yield
    logger.info("Shutting down ML Model Serving Application...")


# Create FastAPI app
app = FastAPI(
    title="ML Model Deployment Service",
    description="A production-ready service for deploying and serving ML models",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "service": "ML Model Deployment Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Comprehensive health check endpoint."""
    all_metrics = metrics_collector.get_metrics()

    model_health = {}
    for name in model_registry:
        health = metrics_collector.check_health(name)
        model_health[name] = {
            **health,
            "loaded": model_registry[name].is_loaded()
        }

    overall_status = "healthy"
    if not model_registry:
        overall_status = "no_models"
    elif any(h.get("status") == "degraded" for h in model_health.values()):
        overall_status = "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        models=model_health,
        uptime_seconds=all_metrics.get("uptime_seconds", 0)
    )


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Kubernetes readiness probe."""
    if not model_registry:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No models loaded"
        )

    loaded_models = [name for name, loader in model_registry.items() if loader.is_loaded()]
    if not loaded_models:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No models ready for inference"
        )

    return {"status": "ready", "loaded_models": loaded_models}


@app.get("/live", tags=["Health"])
async def liveness_check():
    """Kubernetes liveness probe."""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


@app.get("/models", response_model=List[ModelInfo], tags=["Models"])
async def list_models():
    """List all loaded models."""
    models = []
    for name, loader in model_registry.items():
        models.append(ModelInfo(
            name=name,
            format=loader.metadata.get("format", "unknown"),
            loaded=loader.is_loaded(),
            metadata=loader.metadata
        ))
    return models


@app.post("/models/load", tags=["Models"])
async def load_model(model_name: str, model_path: str):
    """Load a model from a file path."""
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model file not found: {model_path}"
        )

    try:
        loader = get_model_loader(model_path)
        loader.load()
        model_registry[model_name] = loader
        metrics_collector.register_model(model_name)

        return {
            "message": f"Model '{model_name}' loaded successfully",
            "metadata": loader.metadata
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load model: {str(e)}"
        )


@app.delete("/models/{model_name}", tags=["Models"])
async def unload_model(model_name: str):
    """Unload a model from memory."""
    if model_name not in model_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model_name}' not found"
        )

    del model_registry[model_name]
    return {"message": f"Model '{model_name}' unloaded successfully"}


@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
async def predict(request: PredictionRequest):
    """Run inference on a loaded model."""
    if request.model_name not in model_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{request.model_name}' not found. Available models: {list(model_registry.keys())}"
        )

    loader = model_registry[request.model_name]
    if not loader.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model '{request.model_name}' is not loaded"
        )

    try:
        # Convert input to numpy array
        input_array = np.array(request.input_data, dtype=np.float32)

        # Time the prediction
        with PredictionTimer(
            metrics_collector,
            request.model_name,
            input_array.shape
        ) as timer:
            predictions = loader.predict(input_array)

        # Calculate latency
        latency_ms = (datetime.utcnow() - datetime.utcnow()).total_seconds() * 1000
        metrics = metrics_collector.get_metrics(request.model_name)
        latency_ms = metrics.get("latency", {}).get("avg_ms", 0)

        return PredictionResponse(
            model_name=request.model_name,
            predictions=predictions.tolist(),
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/metrics", tags=["Monitoring"])
async def get_metrics(model_name: Optional[str] = None):
    """Get model metrics for monitoring."""
    return metrics_collector.get_metrics(model_name)


@app.get("/metrics/{model_name}/latency", tags=["Monitoring"])
async def get_latency_history(model_name: str, count: int = 100):
    """Get recent latency values for a model."""
    if model_name not in model_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model_name}' not found"
        )

    latencies = metrics_collector.get_recent_latencies(model_name, count)
    return {
        "model_name": model_name,
        "latencies": latencies,
        "count": len(latencies),
        "avg_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
