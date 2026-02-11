import json
import os
from typing import Optional, Dict, Any
from src.llm_api.base_client import BaseLLMClient, LLMResponse
from src.anti_hallucination.screener import AntiHallucinationScreener, ScreeningResult

class AntiHallucinationPipeline:
    def __init__(self, client: BaseLLMClient, templates_path: str = "src/anti_hallucination/templates.json"):
        self.client = client
        self.screener = AntiHallucinationScreener()
        self.templates = self._load_templates(templates_path)

    def _load_templates(self, path: str) -> Dict[str, Any]:
        """Loads the JSON templates."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Templates file not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def process(self, query: str, language: str = "en", model: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes a query through the Anti-Hallucination pipeline.

        Returns a dict with:
        - original_response: The raw LLM response.
        - screening_result: The ScreeningResult object.
        - final_answer: The filtered answer (if passed) or a warning.
        """

        # Default to 'en' if language not found
        template_group = self.templates.get(language, self.templates.get("en"))
        if not template_group:
             raise ValueError(f"Template for language '{language}' not found and no 'en' fallback available.")

        system_prompt = template_group["system"]
        user_prompt_template = template_group["user"]

        formatted_user_prompt = user_prompt_template.replace("{query}", query)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": formatted_user_prompt}
        ]

        # Call LLM
        response: LLMResponse = self.client.chat(messages, model=model)
        raw_text = response.content

        # Screen Response
        screening_result = self.screener.check(raw_text)

        final_answer = ""
        if screening_result.passed:
            if screening_result.filtered_response:
                 final_answer = screening_result.filtered_response
            else:
                 final_answer = raw_text # Fallback if filtered response is somehow empty
        else:
            final_answer = f"[WARNING: Anti-Hallucination Check Failed]\nReason: {screening_result.reason}\n\nOriginal Draft:\n{raw_text}"

        return {
            "original_response": raw_text,
            "screening_result": screening_result,
            "final_answer": final_answer,
            "latency_ms": response.latency_ms
        }
