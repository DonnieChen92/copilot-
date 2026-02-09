# ML Model Deployment Service

A production-ready service for deploying and serving machine learning models. Supports multiple model formats (ONNX, TensorFlow, PyTorch, TFLite) with built-in monitoring, health checks, and Kubernetes deployment.

## Features

- **Multi-format Support**: ONNX, TensorFlow SavedModel, PyTorch, TensorFlow Lite
- **FastAPI-based**: High-performance async API with automatic OpenAPI documentation
- **Monitoring**: Built-in metrics collection and health checks
- **Containerized**: Docker and Docker Compose ready
- **Kubernetes Ready**: Complete K8s manifests with HPA, PDB, and Ingress
- **GPU Support**: Optional GPU acceleration with NVIDIA CUDA

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MODEL_PATH=/path/to/your/model.onnx
export MODEL_NAME=my-model

# Run the service
python -m uvicorn app.main:app --reload
```

### Docker

```bash
# Build the image
docker build -t ml-service:latest .

# Run with a model
docker run -p 8000:8000 \
  -v /path/to/models:/app/models \
  -e MODEL_PATH=/app/models/model.onnx \
  ml-service:latest
```

### Docker Compose

```bash
# Start the service
docker-compose up -d ml-service

# Start with monitoring (Prometheus + Grafana)
docker-compose --profile monitoring up -d

# Start GPU-enabled service (requires nvidia-docker)
docker-compose --profile gpu up -d ml-service-gpu
```

### Kubernetes

```bash
# Create namespace and deploy
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/

# Check deployment status
kubectl -n ml-deployment get pods
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check with model status |
| `/live` | GET | Liveness probe |
| `/ready` | GET | Readiness probe |
| `/models` | GET | List loaded models |
| `/models/load` | POST | Load a model |
| `/models/{name}` | DELETE | Unload a model |
| `/predict` | POST | Run inference |
| `/metrics` | GET | Get metrics |

## Prediction Example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "default",
    "input_data": [[1.0, 2.0, 3.0, 4.0]]
  }'
```

## Model Formats

### ONNX (Recommended)
```python
# Export PyTorch model to ONNX
torch.onnx.export(model, dummy_input, "model.onnx")

# Export TensorFlow model to ONNX
python -m tf2onnx.convert --saved-model ./saved_model --output model.onnx
```

### TensorFlow SavedModel
```python
model.save("./saved_model")
```

### PyTorch TorchScript
```python
scripted = torch.jit.script(model)
scripted.save("model.pt")
```

### TensorFlow Lite
```python
converter = tf.lite.TFLiteConverter.from_saved_model("./saved_model")
tflite_model = converter.convert()
with open("model.tflite", "wb") as f:
    f.write(tflite_model)
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | - | Path to model file |
| `MODEL_NAME` | default | Name for the model |
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 8000 | Server port |
| `CORS_ORIGINS` | * | Allowed CORS origins |

## Monitoring

The service exposes metrics at `/metrics`:

- Total predictions count
- Success/failure rates
- Latency (avg, min, max)
- Per-model statistics

Access Grafana at `http://localhost:3000` when using the monitoring profile.

## Scaling

### Horizontal Pod Autoscaler
The included HPA scales based on CPU/memory utilization:
- Min replicas: 2
- Max replicas: 10
- Target CPU: 70%
- Target Memory: 80%

### Manual Scaling
```bash
kubectl -n ml-deployment scale deployment ml-service --replicas=5
```

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
ml_deployment/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── model_loader.py   # Model loading utilities
│   └── monitoring.py     # Metrics collection
├── configs/
│   ├── config.example.env
│   └── prometheus.yml
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   ├── serviceaccount.yaml
│   └── pdb.yaml
├── models/              # Model files (git-ignored)
├── tests/
│   └── test_api.py
├── Dockerfile
├── Dockerfile.gpu
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## License

MIT - Copyright (c) 2025 Jiadong Chen

## Author & Contact

**Owner**: Jiadong Chen (CHEN, JIADONG)
**Email**: donniechen92@gmail.com
**Website**: [jiadongchendonnie.ai](https://jiadongchendonnie.ai)
