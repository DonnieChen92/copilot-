//! AI Product Pipeline - Main Entry Point
//!
//! A multi-model AI orchestration service supporting Claude, Gemini, and Copilot.

mod config;
mod error;
mod handlers;
mod metrics;
mod models;
mod orchestrator;

use axum::{
    routing::{get, post},
    Router,
};
use std::net::SocketAddr;
use tower_http::cors::{Any, CorsLayer};
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "ai_product_pipeline=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Load configuration
    let config = config::Config::load()?;
    tracing::info!("Configuration loaded: {:?}", config.environment);

    // Initialize metrics
    metrics::init_metrics();

    // Build application routes
    let app = Router::new()
        .route("/", get(handlers::root))
        .route("/health", get(handlers::health))
        .route("/ready", get(handlers::ready))
        .route("/metrics", get(handlers::metrics))
        .route("/api/v1/orchestrate", post(handlers::orchestrate))
        .route("/api/v1/models", get(handlers::list_models))
        .route("/api/v1/models/:model_id/invoke", post(handlers::invoke_model))
        .layer(CorsLayer::new().allow_origin(Any).allow_methods(Any))
        .layer(TraceLayer::new_for_http());

    // Start server
    let addr = SocketAddr::from(([0, 0, 0, 0], config.port));
    tracing::info!("Starting AI Product Pipeline on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
