# Deployment Guide

## Prerequisites

- Docker
- Kubernetes cluster (for production)
- Python 3.9+
- Node.js 18+
- Cloud provider account (AWS/GCP/Azure)

## Local Development

### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the server:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment:
```bash
cp .env.example .env.local
# Edit .env.local with API URL
```

4. Run development server:
```bash
npm run dev
```

## Docker Deployment

### Build Images

Backend:
```bash
docker build -t worldtree-api:latest ./backend
```

Frontend:
```bash
docker build -t worldtree-dashboard:latest ./frontend
```

### Run with Docker Compose

```bash
docker-compose up -d
```

## Kubernetes Deployment

### Prerequisites

- kubectl configured
- Access to Kubernetes cluster
- Container registry (ECR, GCR, or ACR)

### Steps

1. Push images to container registry:
```bash
docker tag worldtree-api:latest <registry>/worldtree-api:latest
docker push <registry>/worldtree-api:latest
```

2. Update Kubernetes manifests:
```bash
cd infrastructure/kubernetes
# Edit deployment.yaml with your registry URLs
```

3. Apply manifests:
```bash
kubectl apply -f infrastructure/kubernetes/
```

4. Verify deployment:
```bash
kubectl get pods
kubectl get services
```

## Cloud Provider Setup

### AWS

1. Set up SageMaker:
```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

2. Configure Bedrock access:
- Enable Bedrock in AWS Console
- Request model access for Claude
- Set IAM permissions

### Google Cloud

1. Enable Vertex AI:
```bash
gcloud services enable aiplatform.googleapis.com
```

2. Set up authentication:
```bash
gcloud auth application-default login
```

### Azure

1. Create Azure ML workspace:
```bash
az ml workspace create -w worldtree-workspace -g worldtree-rg
```

2. Configure credentials:
```bash
az ad sp create-for-rbac --name worldtree-sp
```

## Environment Variables

### Backend (.env)
```bash
# Environment
ENVIRONMENT=production
LOG_LEVEL=info

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
AZURE_API_KEY=...

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/worldtree

# Security
JWT_SECRET=your-secret-key
CORS_ORIGINS=https://dashboard.worldtree.ai
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://api.worldtree.ai
```

## Monitoring

### Prometheus

1. Install Prometheus:
```bash
kubectl apply -f infrastructure/kubernetes/monitoring/prometheus.yaml
```

2. Access metrics:
```bash
http://localhost:9090
```

### Grafana

1. Install Grafana:
```bash
kubectl apply -f infrastructure/kubernetes/monitoring/grafana.yaml
```

2. Access dashboard:
```bash
http://localhost:3001
```

## Scaling

### Horizontal Pod Autoscaling

```bash
kubectl autoscale deployment worldtree-api \
  --cpu-percent=70 \
  --min=3 \
  --max=10
```

### Database Scaling

- Set up read replicas
- Configure connection pooling
- Implement caching layer (Redis)

## Security Checklist

- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up API rate limiting
- [ ] Enable audit logging
- [ ] Implement secret management
- [ ] Set up WAF (Web Application Firewall)
- [ ] Configure CORS properly
- [ ] Enable DDoS protection

## Backup & Recovery

### Database Backups

```bash
# Automated daily backups
0 2 * * * pg_dump worldtree > backup-$(date +%Y%m%d).sql
```

### Disaster Recovery

- Cross-region replication
- Regular backup testing
- Documented recovery procedures
- RTO/RPO targets defined

## Troubleshooting

### Common Issues

1. **API not responding**
   - Check pod status: `kubectl get pods`
   - View logs: `kubectl logs <pod-name>`

2. **Model provider errors**
   - Verify API keys
   - Check provider status pages
   - Review rate limits

3. **Database connection issues**
   - Verify connection string
   - Check database status
   - Review network policies

## Support

For deployment issues:
- Check documentation in /docs
- Review issue tracker
- Contact support team
