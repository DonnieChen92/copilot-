//! HTTP handlers for AI Product Pipeline

use axum::{
    extract::Path,
    http::StatusCode,
    Json,
};
use chrono::Utc;
use uuid::Uuid;

use crate::error::PipelineError;
use crate::metrics;
use crate::models::*;
use crate::orchestrator;

/// Root endpoint
pub async fn root() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "service": "AI Product Pipeline",
        "version": env!("CARGO_PKG_VERSION"),
        "docs": "/docs",
        "health": "/health"
    }))
}

/// Health check endpoint
pub async fn health() -> Json<HealthStatus> {
    static START_TIME: std::sync::OnceLock<std::time::Instant> = std::sync::OnceLock::new();
    let start = START_TIME.get_or_init(std::time::Instant::now);

    Json(HealthStatus {
        status: "healthy".to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        uptime_secs: start.elapsed().as_secs(),
        models_available: orchestrator::available_models().len(),
    })
}

/// Readiness probe
pub async fn ready() -> Result<Json<ReadinessStatus>, (StatusCode, &'static str)> {
    let models = orchestrator::available_models();

    if models.is_empty() {
        return Err((StatusCode::SERVICE_UNAVAILABLE, "No models configured"));
    }

    let model_status: Vec<ModelHealthStatus> = models
        .iter()
        .map(|m| ModelHealthStatus {
            model_id: m.id.clone(),
            provider: m.provider.clone(),
            healthy: true, // TODO: implement actual health checks
            last_check: Utc::now(),
        })
        .collect();

    Ok(Json(ReadinessStatus {
        ready: true,
        models: model_status,
    }))
}

/// Prometheus metrics endpoint
pub async fn metrics() -> String {
    metrics::gather_metrics()
}

/// Orchestrate request across models
pub async fn orchestrate(
    Json(request): Json<OrchestrationRequest>,
) -> Result<Json<OrchestrationResponse>, PipelineError> {
    let request_id = Uuid::new_v4();
    let start = std::time::Instant::now();

    tracing::info!(
        request_id = %request_id,
        strategy = ?request.strategy,
        "Processing orchestration request"
    );

    // Record metric
    metrics::increment_requests("orchestrate");

    let results = orchestrator::execute_orchestration(&request).await?;

    let selected = orchestrator::select_result(&results, &request.strategy);

    let response = OrchestrationResponse {
        request_id,
        results: results.clone(),
        selected_result: selected,
        strategy_used: format!("{:?}", request.strategy),
        total_latency_ms: start.elapsed().as_millis() as u64,
        timestamp: Utc::now(),
    };

    // Record latency
    metrics::observe_latency("orchestrate", start.elapsed().as_secs_f64());

    Ok(Json(response))
}

/// List available models
pub async fn list_models() -> Json<Vec<ModelConfig>> {
    Json(orchestrator::available_models())
}

/// Invoke a specific model
pub async fn invoke_model(
    Path(model_id): Path<String>,
    Json(request): Json<ModelInvokeRequest>,
) -> Result<Json<ModelInvokeResponse>, PipelineError> {
    let request_id = Uuid::new_v4();
    let start = std::time::Instant::now();

    tracing::info!(
        request_id = %request_id,
        model_id = %model_id,
        "Invoking model"
    );

    // Record metric
    metrics::increment_requests(&format!("invoke_{}", model_id));

    let result = orchestrator::invoke_single_model(&model_id, &request).await?;

    let response = ModelInvokeResponse {
        request_id,
        model_id: model_id.clone(),
        output: result.output,
        latency_ms: start.elapsed().as_millis() as u64,
        tokens_used: result.tokens_used,
        timestamp: Utc::now(),
    };

    // Record latency
    metrics::observe_latency(&format!("invoke_{}", model_id), start.elapsed().as_secs_f64());

    Ok(Json(response))
}
