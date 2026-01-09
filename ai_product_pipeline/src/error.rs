//! Error types for AI Product Pipeline

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum PipelineError {
    #[error("Model not found: {0}")]
    ModelNotFound(String),

    #[error("Model invocation failed: {0}")]
    ModelInvocationFailed(String),

    #[error("Invalid request: {0}")]
    InvalidRequest(String),

    #[error("Configuration error: {0}")]
    ConfigError(String),

    #[error("Timeout exceeded")]
    Timeout,

    #[error("Rate limit exceeded")]
    RateLimited,

    #[error("Internal error: {0}")]
    Internal(String),
}

impl IntoResponse for PipelineError {
    fn into_response(self) -> Response {
        let (status, error_message) = match &self {
            PipelineError::ModelNotFound(_) => (StatusCode::NOT_FOUND, self.to_string()),
            PipelineError::InvalidRequest(_) => (StatusCode::BAD_REQUEST, self.to_string()),
            PipelineError::Timeout => (StatusCode::GATEWAY_TIMEOUT, self.to_string()),
            PipelineError::RateLimited => (StatusCode::TOO_MANY_REQUESTS, self.to_string()),
            PipelineError::ModelInvocationFailed(_) => {
                (StatusCode::BAD_GATEWAY, self.to_string())
            }
            PipelineError::ConfigError(_) | PipelineError::Internal(_) => {
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".to_string())
            }
        };

        let body = Json(json!({
            "error": error_message,
            "status": status.as_u16()
        }));

        (status, body).into_response()
    }
}
