import unittest
from unittest.mock import MagicMock
from src.llm_api.base_client import BaseLLMClient, LLMResponse
from src.anti_hallucination.pipeline import AntiHallucinationPipeline
from src.anti_hallucination.screener import ScreeningResult

class TestAntiHallucinationPipeline(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=BaseLLMClient)
        # Assuming templates.json is in src/anti_hallucination/
        self.pipeline = AntiHallucinationPipeline(self.mock_client)

    def test_pipeline_success(self):
        """Test a response that passes the screener."""
        good_response_text = """
[Thinking]
I will analyze the request.
Step 1: Check facts.

[Fact Check]
Fact: Python is a language.

[Confidence Score]
90

[Answer]
Python is a programming language.
"""
        self.mock_client.chat.return_value = LLMResponse(
            content=good_response_text,
            latency_ms=100
        )

        result = self.pipeline.process("What is Python?")

        self.assertTrue(result["screening_result"].passed)
        self.assertEqual(result["final_answer"], "Python is a programming language.")
        self.assertEqual(result["screening_result"].confidence_score, 90.0)

    def test_pipeline_low_confidence(self):
        """Test a response that fails due to low confidence."""
        bad_response_text = """
[Thinking]
I am not sure.

[Fact Check]
None.

[Confidence Score]
50

[Answer]
Maybe it is a snake?
"""
        self.mock_client.chat.return_value = LLMResponse(
            content=bad_response_text,
            latency_ms=100
        )

        result = self.pipeline.process("What is Python?")

        self.assertFalse(result["screening_result"].passed)
        self.assertIn("[WARNING: Anti-Hallucination Check Failed]", result["final_answer"])
        self.assertIn("below threshold", result["screening_result"].reason)

    def test_pipeline_missing_sections(self):
        """Test a response that is missing required sections."""
        bad_response_text = "I don't know the format."

        self.mock_client.chat.return_value = LLMResponse(
            content=bad_response_text,
            latency_ms=50
        )

        result = self.pipeline.process("Test")

        self.assertFalse(result["screening_result"].passed)
        self.assertIn("Missing required section", result["screening_result"].reason)

if __name__ == "__main__":
    unittest.main()
