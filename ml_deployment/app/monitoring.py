"""Monitoring and metrics collection for ML model deployment."""
import time
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from threading import Lock

logger = logging.getLogger(__name__)


@dataclass
class PredictionMetrics:
    """Metrics for a single prediction."""
    timestamp: datetime
    latency_ms: float
    input_shape: tuple
    success: bool
    error_message: Optional[str] = None


@dataclass
class ModelMetrics:
    """Aggregated metrics for a model."""
    model_name: str
    total_predictions: int = 0
    successful_predictions: int = 0
    failed_predictions: int = 0
    total_latency_ms: float = 0.0
    min_latency_ms: float = float('inf')
    max_latency_ms: float = 0.0
    last_prediction_time: Optional[datetime] = None
    recent_predictions: deque = field(default_factory=lambda: deque(maxlen=1000))

    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency."""
        if self.total_predictions == 0:
            return 0.0
        return self.total_latency_ms / self.total_predictions

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_predictions == 0:
            return 0.0
        return self.successful_predictions / self.total_predictions * 100

    def to_dict(self) -> Dict:
        """Convert metrics to dictionary."""
        return {
            "model_name": self.model_name,
            "total_predictions": self.total_predictions,
            "successful_predictions": self.successful_predictions,
            "failed_predictions": self.failed_predictions,
            "success_rate_percent": round(self.success_rate, 2),
            "latency": {
                "avg_ms": round(self.avg_latency_ms, 2),
                "min_ms": round(self.min_latency_ms, 2) if self.min_latency_ms != float('inf') else 0,
                "max_ms": round(self.max_latency_ms, 2)
            },
            "last_prediction_time": self.last_prediction_time.isoformat() if self.last_prediction_time else None
        }


class MetricsCollector:
    """Centralized metrics collection for model monitoring."""

    def __init__(self):
        self._metrics: Dict[str, ModelMetrics] = {}
        self._lock = Lock()
        self._start_time = datetime.utcnow()

    def register_model(self, model_name: str) -> None:
        """Register a model for metrics collection."""
        with self._lock:
            if model_name not in self._metrics:
                self._metrics[model_name] = ModelMetrics(model_name=model_name)
                logger.info(f"Registered model '{model_name}' for metrics collection")

    def record_prediction(
        self,
        model_name: str,
        latency_ms: float,
        input_shape: tuple,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """Record a prediction event."""
        with self._lock:
            if model_name not in self._metrics:
                self.register_model(model_name)

            metrics = self._metrics[model_name]
            now = datetime.utcnow()

            # Update counters
            metrics.total_predictions += 1
            if success:
                metrics.successful_predictions += 1
            else:
                metrics.failed_predictions += 1

            # Update latency stats
            metrics.total_latency_ms += latency_ms
            metrics.min_latency_ms = min(metrics.min_latency_ms, latency_ms)
            metrics.max_latency_ms = max(metrics.max_latency_ms, latency_ms)
            metrics.last_prediction_time = now

            # Store recent prediction
            prediction = PredictionMetrics(
                timestamp=now,
                latency_ms=latency_ms,
                input_shape=input_shape,
                success=success,
                error_message=error_message
            )
            metrics.recent_predictions.append(prediction)

    def get_metrics(self, model_name: Optional[str] = None) -> Dict:
        """Get metrics for a model or all models."""
        with self._lock:
            if model_name:
                if model_name not in self._metrics:
                    return {"error": f"Model '{model_name}' not found"}
                return self._metrics[model_name].to_dict()

            return {
                "uptime_seconds": (datetime.utcnow() - self._start_time).total_seconds(),
                "models": {name: m.to_dict() for name, m in self._metrics.items()}
            }

    def get_recent_latencies(self, model_name: str, count: int = 100) -> List[float]:
        """Get recent latency values for drift detection."""
        with self._lock:
            if model_name not in self._metrics:
                return []

            recent = list(self._metrics[model_name].recent_predictions)[-count:]
            return [p.latency_ms for p in recent if p.success]

    def check_health(self, model_name: str) -> Dict:
        """Health check for a model."""
        with self._lock:
            if model_name not in self._metrics:
                return {"status": "unknown", "message": f"Model '{model_name}' not registered"}

            metrics = self._metrics[model_name]

            # Define health thresholds
            if metrics.total_predictions == 0:
                return {"status": "idle", "message": "No predictions recorded yet"}

            if metrics.success_rate < 90:
                return {
                    "status": "degraded",
                    "message": f"Success rate below threshold: {metrics.success_rate:.1f}%"
                }

            if metrics.avg_latency_ms > 1000:
                return {
                    "status": "slow",
                    "message": f"High average latency: {metrics.avg_latency_ms:.0f}ms"
                }

            return {"status": "healthy", "message": "All metrics within normal range"}


class PredictionTimer:
    """Context manager for timing predictions."""

    def __init__(self, collector: MetricsCollector, model_name: str, input_shape: tuple):
        self.collector = collector
        self.model_name = model_name
        self.input_shape = input_shape
        self.start_time = None
        self.success = True
        self.error_message = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        latency_ms = (time.perf_counter() - self.start_time) * 1000

        if exc_type is not None:
            self.success = False
            self.error_message = str(exc_val)

        self.collector.record_prediction(
            model_name=self.model_name,
            latency_ms=latency_ms,
            input_shape=self.input_shape,
            success=self.success,
            error_message=self.error_message
        )

        return False  # Don't suppress exceptions


# Global metrics collector instance
metrics_collector = MetricsCollector()
