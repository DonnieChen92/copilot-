// HTTP Client for AI Pipeline SDK

import Foundation
import AsyncHTTPClient
import NIOCore
import NIOHTTP1
import Logging

/// Pipeline API client
internal actor PipelineClient {
    private let baseURL: String
    private let apiKey: String?
    private let httpClient: HTTPClient
    private let logger: Logger
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    init(baseURL: String, apiKey: String?) {
        self.baseURL = baseURL.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
        self.apiKey = apiKey
        self.httpClient = HTTPClient(eventLoopGroupProvider: .singleton)
        self.logger = Logger(label: "com.aipipeline.client")
        self.decoder = JSONDecoder()
        self.encoder = JSONEncoder()
    }

    deinit {
        try? httpClient.syncShutdown()
    }

    /// List available models
    func listModels() async throws -> [ModelConfig] {
        return try await get(path: "/api/v1/models")
    }

    /// Invoke a specific model
    func invokeModel(modelId: String, request: InvokeRequest) async throws -> ModelResponse {
        return try await post(path: "/api/v1/models/\(modelId)/invoke", body: request)
    }

    /// Orchestrate across models
    func orchestrate(request: OrchestrationRequest) async throws -> OrchestrationResponse {
        return try await post(path: "/api/v1/orchestrate", body: request)
    }

    /// Health check
    func healthCheck() async throws -> HealthStatus {
        return try await get(path: "/health")
    }

    // MARK: - Private HTTP methods

    private func get<T: Decodable>(path: String) async throws -> T {
        var request = HTTPClientRequest(url: "\(baseURL)\(path)")
        request.method = .GET
        addHeaders(to: &request)

        logger.debug("GET \(path)")

        let response = try await httpClient.execute(request, timeout: .seconds(30))
        return try await decodeResponse(response)
    }

    private func post<T: Decodable, B: Encodable>(path: String, body: B) async throws -> T {
        var request = HTTPClientRequest(url: "\(baseURL)\(path)")
        request.method = .POST
        addHeaders(to: &request)

        let bodyData = try encoder.encode(body)
        request.body = .bytes(ByteBuffer(data: bodyData))

        logger.debug("POST \(path)")

        let response = try await httpClient.execute(request, timeout: .seconds(30))
        return try await decodeResponse(response)
    }

    private func addHeaders(to request: inout HTTPClientRequest) {
        request.headers.add(name: "Content-Type", value: "application/json")
        request.headers.add(name: "Accept", value: "application/json")
        request.headers.add(name: "User-Agent", value: "AIPipeline-Swift/\(AIPipeline.version)")

        if let apiKey = apiKey {
            request.headers.add(name: "Authorization", value: "Bearer \(apiKey)")
        }
    }

    private func decodeResponse<T: Decodable>(_ response: HTTPClientResponse) async throws -> T {
        let body = try await response.body.collect(upTo: 10 * 1024 * 1024) // 10MB max

        guard response.status == .ok else {
            let errorMessage = String(buffer: body)
            logger.error("API error: \(response.status) - \(errorMessage)")
            throw PipelineError.apiError(status: Int(response.status.code), message: errorMessage)
        }

        do {
            return try decoder.decode(T.self, from: Data(buffer: body))
        } catch {
            logger.error("Decode error: \(error)")
            throw PipelineError.decodingError(error)
        }
    }
}

/// Pipeline SDK errors
public enum PipelineError: Error, LocalizedError {
    case apiError(status: Int, message: String)
    case decodingError(Error)
    case networkError(Error)
    case invalidURL

    public var errorDescription: String? {
        switch self {
        case .apiError(let status, let message):
            return "API Error (\(status)): \(message)"
        case .decodingError(let error):
            return "Decoding Error: \(error.localizedDescription)"
        case .networkError(let error):
            return "Network Error: \(error.localizedDescription)"
        case .invalidURL:
            return "Invalid URL"
        }
    }
}
