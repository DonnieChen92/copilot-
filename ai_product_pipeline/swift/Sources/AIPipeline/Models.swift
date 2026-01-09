// Data models for AI Pipeline SDK

import Foundation

/// Supported AI model providers
public enum ModelProvider: String, Codable, Sendable {
    case claude
    case gemini
    case copilot
    case custom
}

/// Model configuration
public struct ModelConfig: Codable, Sendable {
    public let id: String
    public let provider: ModelProvider
    public let modelName: String
    public let endpoint: String?
    public let maxTokens: Int
    public let temperature: Double
    public let capabilities: [String]

    enum CodingKeys: String, CodingKey {
        case id
        case provider
        case modelName = "model_name"
        case endpoint
        case maxTokens = "max_tokens"
        case temperature
        case capabilities
    }
}

/// Orchestration strategy
public enum OrchestrationStrategy: String, Codable, Sendable {
    case firstSuccess = "first_success"
    case bestScore = "best_score"
    case consensus
    case chain
}

/// Request for orchestration
public struct OrchestrationRequest: Codable, Sendable {
    public let prompt: String
    public let models: [String]?
    public let strategy: OrchestrationStrategy
    public let context: [String: String]?

    public init(prompt: String, models: [String]?, strategy: OrchestrationStrategy, context: [String: String]?) {
        self.prompt = prompt
        self.models = models
        self.strategy = strategy
        self.context = context
    }
}

/// Response from orchestration
public struct OrchestrationResponse: Codable, Sendable {
    public let requestId: String
    public let results: [ModelResult]
    public let selectedResult: ModelResult?
    public let strategyUsed: String
    public let totalLatencyMs: Int
    public let timestamp: String

    enum CodingKeys: String, CodingKey {
        case requestId = "request_id"
        case results
        case selectedResult = "selected_result"
        case strategyUsed = "strategy_used"
        case totalLatencyMs = "total_latency_ms"
        case timestamp
    }
}

/// Result from a single model
public struct ModelResult: Codable, Sendable {
    public let modelId: String
    public let provider: ModelProvider
    public let output: String
    public let latencyMs: Int
    public let tokensUsed: Int?
    public let score: Double?
    public let success: Bool
    public let error: String?

    enum CodingKeys: String, CodingKey {
        case modelId = "model_id"
        case provider
        case output
        case latencyMs = "latency_ms"
        case tokensUsed = "tokens_used"
        case score
        case success
        case error
    }
}

/// Request for model invocation
public struct InvokeRequest: Codable, Sendable {
    public let prompt: String
    public let maxTokens: Int?
    public let temperature: Double?
    public let context: [String: String]?

    enum CodingKeys: String, CodingKey {
        case prompt
        case maxTokens = "max_tokens"
        case temperature
        case context
    }

    public init(prompt: String, maxTokens: Int?, temperature: Double?, context: [String: Any]?) {
        self.prompt = prompt
        self.maxTokens = maxTokens
        self.temperature = temperature
        // Convert context to string dictionary
        self.context = context?.compactMapValues { "\($0)" }
    }
}

/// Response from model invocation
public struct ModelResponse: Codable, Sendable {
    public let requestId: String
    public let modelId: String
    public let output: String
    public let latencyMs: Int
    public let tokensUsed: Int?
    public let timestamp: String

    enum CodingKeys: String, CodingKey {
        case requestId = "request_id"
        case modelId = "model_id"
        case output
        case latencyMs = "latency_ms"
        case tokensUsed = "tokens_used"
        case timestamp
    }
}

/// Health status
public struct HealthStatus: Codable, Sendable {
    public let status: String
    public let version: String
    public let uptimeSecs: Int
    public let modelsAvailable: Int

    enum CodingKeys: String, CodingKey {
        case status
        case version
        case uptimeSecs = "uptime_secs"
        case modelsAvailable = "models_available"
    }
}
