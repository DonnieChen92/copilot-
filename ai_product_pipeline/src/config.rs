//! Configuration management for AI Product Pipeline

use serde::Deserialize;
use std::env;

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub environment: Environment,
    pub port: u16,
    pub claude_api_key: Option<String>,
    pub gemini_api_key: Option<String>,
    pub azure_api_key: Option<String>,
    pub model_timeout_secs: u64,
    pub max_concurrent_requests: usize,
}

#[derive(Debug, Clone, Deserialize, PartialEq)]
#[serde(rename_all = "lowercase")]
pub enum Environment {
    Dev,
    Staging,
    Prod,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            environment: Environment::Dev,
            port: 8080,
            claude_api_key: None,
            gemini_api_key: None,
            azure_api_key: None,
            model_timeout_secs: 30,
            max_concurrent_requests: 100,
        }
    }
}

impl Config {
    pub fn load() -> anyhow::Result<Self> {
        dotenvy::dotenv().ok();

        let environment = match env::var("ENVIRONMENT")
            .unwrap_or_else(|_| "dev".to_string())
            .as_str()
        {
            "prod" | "production" => Environment::Prod,
            "staging" => Environment::Staging,
            _ => Environment::Dev,
        };

        Ok(Self {
            environment,
            port: env::var("PORT")
                .ok()
                .and_then(|p| p.parse().ok())
                .unwrap_or(8080),
            claude_api_key: env::var("CLAUDE_API_KEY").ok(),
            gemini_api_key: env::var("GEMINI_API_KEY").ok(),
            azure_api_key: env::var("AZURE_API_KEY").ok(),
            model_timeout_secs: env::var("MODEL_TIMEOUT_SECS")
                .ok()
                .and_then(|t| t.parse().ok())
                .unwrap_or(30),
            max_concurrent_requests: env::var("MAX_CONCURRENT_REQUESTS")
                .ok()
                .and_then(|m| m.parse().ok())
                .unwrap_or(100),
        })
    }
}
