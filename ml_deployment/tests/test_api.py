"""API tests for ML Model Deployment Service."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_root(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["version"] == "1.0.0"

    def test_liveness(self, client):
        """Test liveness probe."""
        response = client.get("/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    def test_health(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "uptime_seconds" in data


class TestModelsEndpoints:
    """Tests for model management endpoints."""

    def test_list_models_empty(self, client):
        """Test listing models when none are loaded."""
        response = client.get("/models")
        assert response.status_code == 200
        assert response.json() == []


class TestMetricsEndpoints:
    """Tests for metrics endpoints."""

    def test_get_metrics(self, client):
        """Test getting metrics."""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
