//! Data models for AI Product Pipeline

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Supported AI model providers
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum ModelProvider {
    Claude,
    Gemini,
    Copilot,
    Custom(String),
}

/// Model configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ModelConfig {
    pub id: String,
    pub provider: ModelProvider,
    pub model_name: String,
    pub endpoint: Option<String>,
    pub max_tokens: u32,
    pub temperature: f32,
    pub capabilities: Vec<String>,
}

/// Request to orchestrate across models
#[derive(Debug, Deserialize)]
pub struct OrchestrationRequest {
    pub prompt: String,
    pub models: Option<Vec<String>>,
    pub strategy: OrchestrationStrategy,
    pub context: Option<serde_json::Value>,
}

/// How to combine multiple model outputs
#[derive(Debug, Clone, Deserialize, Default)]
#[serde(rename_all = "snake_case")]
pub enum OrchestrationStrategy {
    /// Use the first successful response
    #[default]
    FirstSuccess,
    /// Run all models and return best by score
    BestScore,
    /// Run all models and merge outputs
    Consensus,
    /// Chain models in sequence
    Chain,
}

/// Response from orchestration
#[derive(Debug, Serialize)]
pub struct OrchestrationResponse {
    pub request_id: Uuid,
    pub results: Vec<ModelResult>,
    pub selected_result: Option<ModelResult>,
    pub strategy_used: String,
    pub total_latency_ms: u64,
    pub timestamp: DateTime<Utc>,
}

/// Result from a single model invocation
#[derive(Debug, Clone, Serialize)]
pub struct ModelResult {
    pub model_id: String,
    pub provider: ModelProvider,
    pub output: String,
    pub latency_ms: u64,
    pub tokens_used: Option<u32>,
    pub score: Option<f32>,
    pub success: bool,
    pub error: Option<String>,
}

/// Request to invoke a specific model
#[derive(Debug, Deserialize)]
pub struct ModelInvokeRequest {
    pub prompt: String,
    pub max_tokens: Option<u32>,
    pub temperature: Option<f32>,
    pub context: Option<serde_json::Value>,
}

/// Response from model invocation
#[derive(Debug, Serialize)]
pub struct ModelInvokeResponse {
    pub request_id: Uuid,
    pub model_id: String,
    pub output: String,
    pub latency_ms: u64,
    pub tokens_used: Option<u32>,
    pub timestamp: DateTime<Utc>,
}

/// Health status
#[derive(Debug, Serialize)]
pub struct HealthStatus {
    pub status: String,
    pub version: String,
    pub uptime_secs: u64,
    pub models_available: usize,
}

/// Readiness status
#[derive(Debug, Serialize)]
pub struct ReadinessStatus {
    pub ready: bool,
    pub models: Vec<ModelHealthStatus>,
}

#[derive(Debug, Serialize)]
pub struct ModelHealthStatus {
    pub model_id: String,
    pub provider: ModelProvider,
    pub healthy: bool,
    pub last_check: DateTime<Utc>,
}
