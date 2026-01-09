// AI Product Pipeline - Swift Client SDK
// Provides native Swift integration for iOS/macOS applications

import Foundation
import AsyncHTTPClient
import Logging

/// Main entry point for the AI Pipeline SDK
public struct AIPipeline {
    /// SDK version
    public static let version = "1.0.0"

    private let client: PipelineClient
    private let logger: Logger

    /// Initialize the AI Pipeline SDK
    /// - Parameters:
    ///   - baseURL: Base URL of the AI Pipeline service
    ///   - apiKey: Optional API key for authentication
    public init(baseURL: String = "http://localhost:8080", apiKey: String? = nil) {
        self.client = PipelineClient(baseURL: baseURL, apiKey: apiKey)
        self.logger = Logger(label: "com.aipipeline.sdk")
    }

    /// List available models
    public func listModels() async throws -> [ModelConfig] {
        logger.info("Fetching available models")
        return try await client.listModels()
    }

    /// Invoke a specific model
    /// - Parameters:
    ///   - modelId: The model identifier
    ///   - prompt: The prompt to send
    ///   - options: Optional invocation options
    public func invoke(
        modelId: String,
        prompt: String,
        options: InvokeOptions? = nil
    ) async throws -> ModelResponse {
        logger.info("Invoking model", metadata: ["model_id": "\(modelId)"])
        return try await client.invokeModel(
            modelId: modelId,
            request: InvokeRequest(
                prompt: prompt,
                maxTokens: options?.maxTokens,
                temperature: options?.temperature,
                context: options?.context
            )
        )
    }

    /// Orchestrate a request across multiple models
    /// - Parameters:
    ///   - prompt: The prompt to process
    ///   - strategy: Orchestration strategy
    ///   - models: Optional list of model IDs to use
    public func orchestrate(
        prompt: String,
        strategy: OrchestrationStrategy = .firstSuccess,
        models: [String]? = nil
    ) async throws -> OrchestrationResponse {
        logger.info("Orchestrating request", metadata: ["strategy": "\(strategy)"])
        return try await client.orchestrate(
            request: OrchestrationRequest(
                prompt: prompt,
                models: models,
                strategy: strategy,
                context: nil
            )
        )
    }

    /// Check service health
    public func healthCheck() async throws -> HealthStatus {
        return try await client.healthCheck()
    }
}

/// Options for model invocation
public struct InvokeOptions {
    public let maxTokens: Int?
    public let temperature: Double?
    public let context: [String: Any]?

    public init(maxTokens: Int? = nil, temperature: Double? = nil, context: [String: Any]? = nil) {
        self.maxTokens = maxTokens
        self.temperature = temperature
        self.context = context
    }
}
