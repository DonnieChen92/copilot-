# Deployment Guide for SACA

This guide outlines the steps to deploy the **Sentient Agent Cognitive Architecture (SACA)** orchestration engine.

## Prerequisites

*   **Docker**: Ensure Docker is installed and running on your system.
*   **Python 3.11+**: For local development.

## 1. Local Deployment (Direct)

To run the application locally without Docker:

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    uvicorn saca.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
    Access the interactive docs at `http://localhost:8000/docs`.

## 2. Docker Deployment (Containerized)

To build and run the SACA container:

1.  **Build the Docker image:**
    ```bash
    docker build -t saca-engine:latest .
    ```

2.  **Run the container:**
    ```bash
    docker run -d -p 8000:8000 --name saca-instance saca-engine:latest
    ```

3.  **Verify running container:**
    ```bash
    docker ps
    ```
    Visit `http://localhost:8000` to verify the system status.

## 3. Cloud Deployment (General)

### AWS (Elastic Container Service / App Runner)
1.  Push the Docker image to Amazon ECR.
2.  Deploy using AWS App Runner (easiest) or ECS (more control).
3.  Ensure the security group allows inbound traffic on port 8000 (or mapped port).

### Google Cloud (Cloud Run)
1.  Build and submit the image to Google Container Registry (GCR) or Artifact Registry.
    ```bash
    gcloud builds submit --tag gcr.io/PROJECT-ID/saca-engine
    ```
2.  Deploy to Cloud Run.
    ```bash
    gcloud run deploy saca-service --image gcr.io/PROJECT-ID/saca-engine --platform managed
    ```

### Azure (Container Apps)
1.  Push image to Azure Container Registry (ACR).
2.  Create a Container App via the Azure Portal or CLI using the image from ACR.

## 4. Monitoring & Scaling

*   **Monitoring**: The application exposes a basic health check at `/`. Integrate with Prometheus/Grafana or cloud-native monitoring tools (CloudWatch, Stackdriver) for metrics.
*   **Scaling**: The Docker container is stateless. Use Kubernetes (K8s) or cloud serverless scaling (Cloud Run/App Runner) to increase the number of replicas based on load.
