// AI Pipeline CLI Tool

import ArgumentParser
import AIPipeline
import Foundation

@main
struct AIPipelineCLI: AsyncParsableCommand {
    static var configuration = CommandConfiguration(
        commandName: "ai-pipeline",
        abstract: "CLI for interacting with the AI Product Pipeline",
        version: AIPipeline.version,
        subcommands: [
            ListModels.self,
            Invoke.self,
            Orchestrate.self,
            Health.self
        ],
        defaultSubcommand: Health.self
    )
}

struct GlobalOptions: ParsableArguments {
    @Option(name: .long, help: "Base URL of the pipeline service")
    var url: String = "http://localhost:8080"

    @Option(name: .long, help: "API key for authentication")
    var apiKey: String?
}

struct ListModels: AsyncParsableCommand {
    static var configuration = CommandConfiguration(
        commandName: "models",
        abstract: "List available AI models"
    )

    @OptionGroup var globals: GlobalOptions

    mutating func run() async throws {
        let pipeline = AIPipeline(baseURL: globals.url, apiKey: globals.apiKey)
        let models = try await pipeline.listModels()

        print("Available Models:")
        print(String(repeating: "-", count: 60))
        for model in models {
            print("ID: \(model.id)")
            print("  Provider: \(model.provider)")
            print("  Model: \(model.modelName)")
            print("  Capabilities: \(model.capabilities.joined(separator: ", "))")
            print("")
        }
    }
}

struct Invoke: AsyncParsableCommand {
    static var configuration = CommandConfiguration(
        commandName: "invoke",
        abstract: "Invoke a specific model"
    )

    @OptionGroup var globals: GlobalOptions

    @Option(name: .shortAndLong, help: "Model ID to invoke")
    var model: String

    @Argument(help: "Prompt to send to the model")
    var prompt: String

    @Option(name: .long, help: "Maximum tokens")
    var maxTokens: Int?

    @Option(name: .long, help: "Temperature (0.0-1.0)")
    var temperature: Double?

    mutating func run() async throws {
        let pipeline = AIPipeline(baseURL: globals.url, apiKey: globals.apiKey)

        let options = InvokeOptions(
            maxTokens: maxTokens,
            temperature: temperature,
            context: nil
        )

        let response = try await pipeline.invoke(
            modelId: model,
            prompt: prompt,
            options: options
        )

        print("Response from \(response.modelId):")
        print(String(repeating: "-", count: 60))
        print(response.output)
        print(String(repeating: "-", count: 60))
        print("Latency: \(response.latencyMs)ms")
        if let tokens = response.tokensUsed {
            print("Tokens used: \(tokens)")
        }
    }
}

struct Orchestrate: AsyncParsableCommand {
    static var configuration = CommandConfiguration(
        commandName: "orchestrate",
        abstract: "Orchestrate across multiple models"
    )

    @OptionGroup var globals: GlobalOptions

    @Argument(help: "Prompt to process")
    var prompt: String

    @Option(name: .shortAndLong, help: "Strategy: first_success, best_score, consensus, chain")
    var strategy: String = "first_success"

    @Option(name: .shortAndLong, parsing: .upToNextOption, help: "Specific model IDs to use")
    var models: [String] = []

    mutating func run() async throws {
        let pipeline = AIPipeline(baseURL: globals.url, apiKey: globals.apiKey)

        let orchestrationStrategy: OrchestrationStrategy = switch strategy {
        case "best_score": .bestScore
        case "consensus": .consensus
        case "chain": .chain
        default: .firstSuccess
        }

        let response = try await pipeline.orchestrate(
            prompt: prompt,
            strategy: orchestrationStrategy,
            models: models.isEmpty ? nil : models
        )

        print("Orchestration Results:")
        print(String(repeating: "-", count: 60))
        print("Strategy: \(response.strategyUsed)")
        print("Total Latency: \(response.totalLatencyMs)ms")
        print("")

        if let selected = response.selectedResult {
            print("Selected Result (\(selected.modelId)):")
            print(selected.output)
        }

        print("")
        print("All Results:")
        for result in response.results {
            print("  - \(result.modelId): \(result.success ? "success" : "failed") (\(result.latencyMs)ms)")
        }
    }
}

struct Health: AsyncParsableCommand {
    static var configuration = CommandConfiguration(
        commandName: "health",
        abstract: "Check service health"
    )

    @OptionGroup var globals: GlobalOptions

    mutating func run() async throws {
        let pipeline = AIPipeline(baseURL: globals.url, apiKey: globals.apiKey)
        let health = try await pipeline.healthCheck()

        print("Service Health:")
        print(String(repeating: "-", count: 40))
        print("Status: \(health.status)")
        print("Version: \(health.version)")
        print("Uptime: \(health.uptimeSecs)s")
        print("Models Available: \(health.modelsAvailable)")
    }
}
