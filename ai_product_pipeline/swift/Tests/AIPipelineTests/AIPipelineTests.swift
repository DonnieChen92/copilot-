import XCTest
@testable import AIPipeline

final class AIPipelineTests: XCTestCase {
    func testSDKInitialization() {
        let pipeline = AIPipeline(baseURL: "http://localhost:8080")
        XCTAssertEqual(AIPipeline.version, "1.0.0")
    }

    func testOrchestrationStrategyEncoding() throws {
        let encoder = JSONEncoder()

        let strategies: [OrchestrationStrategy] = [.firstSuccess, .bestScore, .consensus, .chain]

        for strategy in strategies {
            let request = OrchestrationRequest(
                prompt: "test",
                models: nil,
                strategy: strategy,
                context: nil
            )
            let data = try encoder.encode(request)
            let json = String(data: data, encoding: .utf8)!
            XCTAssertTrue(json.contains("strategy"))
        }
    }

    func testModelConfigDecoding() throws {
        let json = """
        {
            "id": "claude-3-opus",
            "provider": "claude",
            "model_name": "claude-3-opus-20240229",
            "endpoint": "https://api.anthropic.com/v1/messages",
            "max_tokens": 4096,
            "temperature": 0.7,
            "capabilities": ["reasoning", "coding"]
        }
        """

        let decoder = JSONDecoder()
        let config = try decoder.decode(ModelConfig.self, from: json.data(using: .utf8)!)

        XCTAssertEqual(config.id, "claude-3-opus")
        XCTAssertEqual(config.provider, .claude)
        XCTAssertEqual(config.maxTokens, 4096)
        XCTAssertEqual(config.capabilities.count, 2)
    }

    func testInvokeOptionsInitialization() {
        let options = InvokeOptions(maxTokens: 1000, temperature: 0.5)
        XCTAssertEqual(options.maxTokens, 1000)
        XCTAssertEqual(options.temperature, 0.5)
    }
}
