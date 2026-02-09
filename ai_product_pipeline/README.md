# AI Product Pipeline

A production-ready AI orchestration service for deploying and managing multi-model AI workflows. Supports Claude, Gemini, and Copilot with comprehensive deployment automation, scoring, and evidence generation.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Product Pipeline                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Claude    │  │   Gemini    │  │   Copilot   │         │
│  │   API       │  │   API       │  │   API       │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│                   ┌──────┴──────┐                          │
│                   │ Orchestrator │                          │
│                   │  (Rust/Swift)│                          │
│                   └──────┬──────┘                          │
│                          │                                  │
│                   ┌──────┴──────┐                          │
│                   │  REST API   │                          │
│                   │  (FastAPI)  │                          │
│                   └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## Features

- **Multi-Model Orchestration**: Route requests across Claude, Gemini, and Copilot
- **Orchestration Strategies**: FirstSuccess, BestScore, Consensus, Chain
- **Rust Backend**: High-performance async API with Axum
- **Swift SDK**: Native iOS/macOS integration
- **AI-Driven Deployment**: Automated deployment with scoring and evidence
- **Zero-Trust Gates**: Quality gates with security/compliance/performance thresholds
- **Kubernetes Ready**: Complete K8s manifests with HPA, PDB, NetworkPolicy

## Quick Start

### Run Locally (Rust)

```bash
# Build and run
cargo build --release
ENVIRONMENT=dev PORT=8080 ./target/release/ai_product_pipeline

# With API keys
export CLAUDE_API_KEY=your_key
export GEMINI_API_KEY=your_key
cargo run
```

### Docker

```bash
# Build and run
docker-compose up -d ai-pipeline

# With ML service integration
docker-compose --profile ml up -d

# With monitoring
docker-compose --profile monitoring up -d
```

### Kubernetes

```bash
# Deploy to cluster
kubectl apply -f deploy/k8s/

# Check status
kubectl -n ai-pipeline get pods
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/ready` | GET | Readiness probe |
| `/metrics` | GET | Prometheus metrics |
| `/api/v1/models` | GET | List available models |
| `/api/v1/models/:id/invoke` | POST | Invoke specific model |
| `/api/v1/orchestrate` | POST | Multi-model orchestration |

## Orchestration Example

```bash
curl -X POST http://localhost:8080/api/v1/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "strategy": "best_score",
    "models": ["claude-3-opus", "gemini-2-flash"]
  }'
```

## AI-Driven Deployment

The `deploy.sh` script provides comprehensive deployment automation:

```bash
# Staging deployment
./deploy.sh --mode agent --env staging --namespace ai-pipeline

# Production (requires approval)
./deploy.sh --mode agent --env prod --approve-prod

# Digital twin simulation
./deploy.sh --mode digital_twin --env prod

# Dry run
./deploy.sh --mode agent --env staging --dry-run
```

### Deployment Phases

1. **Prepare**: Configuration validation
2. **Plan**: NLP-based requirement analysis
3. **Build**: Rust + Swift compilation
4. **Validate**: Tests, security, compliance, performance
5. **Drill**: Tabletop and chaos exercises
6. **Package/Deploy**: Artifact creation and rollout
7. **Evolve**: Evidence persistence

### Scoring System

| Dimension | Weight | Threshold |
|-----------|--------|-----------|
| Security | 30% | 80% |
| Compliance | 20% | 80% |
| Performance | 20% | 80% |
| Quality | 30% | 80% |
| **Overall** | - | **85%** |

### Safety Zones

- 🟢 **Green**: ≥90% - Optimal
- 🟡 **Yellow**: ≥80% - Acceptable
- 🟠 **Orange**: ≥70% - Warning
- 🔴 **Red**: <70% - Blocked

## Swift SDK

```swift
import AIPipeline

let pipeline = AIPipeline(baseURL: "http://localhost:8080")

// List models
let models = try await pipeline.listModels()

// Invoke model
let response = try await pipeline.invoke(
    modelId: "claude-3-opus",
    prompt: "Hello, world!",
    options: InvokeOptions(maxTokens: 1000)
)

// Orchestrate
let result = try await pipeline.orchestrate(
    prompt: "Analyze this code",
    strategy: .bestScore
)
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | dev | dev/staging/prod |
| `PORT` | 8080 | Server port |
| `CLAUDE_API_KEY` | - | Anthropic API key |
| `GEMINI_API_KEY` | - | Google API key |
| `AZURE_API_KEY` | - | Azure/OpenAI key |
| `MODEL_TIMEOUT_SECS` | 30 | Request timeout |
| `MAX_CONCURRENT_REQUESTS` | 100 | Concurrency limit |

## Project Structure

```
ai_product_pipeline/
├── deploy.sh              # AI-driven deployment script
├── Cargo.toml             # Rust dependencies
├── Dockerfile             # Container build
├── docker-compose.yaml    # Local development
├── src/                   # Rust source
│   ├── main.rs
│   ├── config.rs
│   ├── error.rs
│   ├── handlers.rs
│   ├── metrics.rs
│   ├── models.rs
│   └── orchestrator.rs
├── swift/                 # Swift SDK
│   ├── Package.swift
│   └── Sources/
├── deploy/
│   ├── k8s/              # Kubernetes manifests
│   └── prometheus.yml
├── evidence/             # Deployment evidence (generated)
└── tests/
```

## License

MIT - Copyright (c) 2025 Jiadong Chen

## Author & Contact

**Owner**: Jiadong Chen (CHEN, JIADONG)
**Email**: donniechen92@gmail.com
**Website**: [jiadongchendonnie.ai](https://jiadongchendonnie.ai)
