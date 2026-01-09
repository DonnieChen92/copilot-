//! Model orchestration logic for AI Product Pipeline

use crate::error::PipelineError;
use crate::models::*;

/// Get list of available models
pub fn available_models() -> Vec<ModelConfig> {
    vec![
        ModelConfig {
            id: "claude-3-opus".to_string(),
            provider: ModelProvider::Claude,
            model_name: "claude-3-opus-20240229".to_string(),
            endpoint: Some("https://api.anthropic.com/v1/messages".to_string()),
            max_tokens: 4096,
            temperature: 0.7,
            capabilities: vec![
                "reasoning".to_string(),
                "coding".to_string(),
                "analysis".to_string(),
            ],
        },
        ModelConfig {
            id: "claude-3-sonnet".to_string(),
            provider: ModelProvider::Claude,
            model_name: "claude-3-sonnet-20240229".to_string(),
            endpoint: Some("https://api.anthropic.com/v1/messages".to_string()),
            max_tokens: 4096,
            temperature: 0.7,
            capabilities: vec![
                "reasoning".to_string(),
                "coding".to_string(),
                "general".to_string(),
            ],
        },
        ModelConfig {
            id: "gemini-2-flash".to_string(),
            provider: ModelProvider::Gemini,
            model_name: "gemini-2.0-flash".to_string(),
            endpoint: Some("https://generativelanguage.googleapis.com/v1beta/models".to_string()),
            max_tokens: 8192,
            temperature: 0.7,
            capabilities: vec![
                "multimodal".to_string(),
                "reasoning".to_string(),
                "coding".to_string(),
            ],
        },
        ModelConfig {
            id: "copilot".to_string(),
            provider: ModelProvider::Copilot,
            model_name: "gpt-4".to_string(),
            endpoint: Some("https://api.openai.com/v1/chat/completions".to_string()),
            max_tokens: 4096,
            temperature: 0.7,
            capabilities: vec!["coding".to_string(), "completion".to_string()],
        },
    ]
}

/// Execute orchestration across multiple models
pub async fn execute_orchestration(
    request: &OrchestrationRequest,
) -> Result<Vec<ModelResult>, PipelineError> {
    let models = available_models();
    let target_models: Vec<&ModelConfig> = match &request.models {
        Some(model_ids) => models
            .iter()
            .filter(|m| model_ids.contains(&m.id))
            .collect(),
        None => models.iter().collect(),
    };

    if target_models.is_empty() {
        return Err(PipelineError::ModelNotFound(
            "No matching models found".to_string(),
        ));
    }

    let mut results = Vec::new();

    match request.strategy {
        OrchestrationStrategy::FirstSuccess => {
            for model in target_models {
                let result = invoke_model_internal(model, &request.prompt).await;
                if result.success {
                    results.push(result);
                    break;
                }
                results.push(result);
            }
        }
        OrchestrationStrategy::BestScore | OrchestrationStrategy::Consensus => {
            // Run all models in parallel
            let futures: Vec<_> = target_models
                .iter()
                .map(|model| invoke_model_internal(model, &request.prompt))
                .collect();

            results = futures::future::join_all(futures).await;
        }
        OrchestrationStrategy::Chain => {
            let mut context = request.prompt.clone();
            for model in target_models {
                let result = invoke_model_internal(model, &context).await;
                if result.success {
                    context = result.output.clone();
                }
                results.push(result);
            }
        }
    }

    Ok(results)
}

/// Select best result based on strategy
pub fn select_result(
    results: &[ModelResult],
    strategy: &OrchestrationStrategy,
) -> Option<ModelResult> {
    match strategy {
        OrchestrationStrategy::FirstSuccess => results.iter().find(|r| r.success).cloned(),
        OrchestrationStrategy::BestScore => results
            .iter()
            .filter(|r| r.success)
            .max_by(|a, b| {
                a.score
                    .unwrap_or(0.0)
                    .partial_cmp(&b.score.unwrap_or(0.0))
                    .unwrap_or(std::cmp::Ordering::Equal)
            })
            .cloned(),
        OrchestrationStrategy::Consensus => {
            // Return the most common successful response (simplified)
            results.iter().find(|r| r.success).cloned()
        }
        OrchestrationStrategy::Chain => results.last().cloned(),
    }
}

/// Invoke a single model by ID
pub async fn invoke_single_model(
    model_id: &str,
    request: &ModelInvokeRequest,
) -> Result<ModelResult, PipelineError> {
    let models = available_models();
    let model = models
        .iter()
        .find(|m| m.id == model_id)
        .ok_or_else(|| PipelineError::ModelNotFound(model_id.to_string()))?;

    Ok(invoke_model_internal(model, &request.prompt).await)
}

/// Internal model invocation
async fn invoke_model_internal(model: &ModelConfig, prompt: &str) -> ModelResult {
    let start = std::time::Instant::now();

    // Simulate model invocation (replace with actual API calls)
    // In production, this would make HTTP requests to the respective APIs
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

    let output = format!(
        "[{} response] Processed: {}...",
        model.model_name,
        &prompt.chars().take(50).collect::<String>()
    );

    ModelResult {
        model_id: model.id.clone(),
        provider: model.provider.clone(),
        output,
        latency_ms: start.elapsed().as_millis() as u64,
        tokens_used: Some(prompt.len() as u32 / 4), // Rough estimate
        score: Some(0.85), // Placeholder score
        success: true,
        error: None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_available_models() {
        let models = available_models();
        assert!(!models.is_empty());
        assert!(models.iter().any(|m| m.provider == ModelProvider::Claude));
    }

    #[tokio::test]
    async fn test_invoke_model() {
        let request = ModelInvokeRequest {
            prompt: "Test prompt".to_string(),
            max_tokens: None,
            temperature: None,
            context: None,
        };

        let result = invoke_single_model("claude-3-opus", &request).await;
        assert!(result.is_ok());
        assert!(result.unwrap().success);
    }
}
