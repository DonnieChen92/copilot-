import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class ScreeningResult:
    passed: bool
    confidence_score: float
    reason: str
    filtered_response: Optional[str] = None

class AntiHallucinationScreener:
    def __init__(self, confidence_threshold: float = 70.0):
        self.confidence_threshold = confidence_threshold

    def parse_response(self, response_text: str) -> dict:
        """
        Parses the structured response into components.
        Expected format:
        [Thinking] ...
        [Fact Check] ...
        [Confidence Score] ...
        [Answer] ...
        """
        sections = {}

        # Regex to capture sections
        # We look for [Header] and capture everything until the next [Header] or end of string.
        pattern = r"\[(.*?)\]\s*(.*?)(?=\n\[|$)"
        matches = re.findall(pattern, response_text, re.DOTALL)

        for header, content in matches:
            sections[header.strip()] = content.strip()

        return sections

    def check(self, response_text: str) -> ScreeningResult:
        """
        Screens the response for hallucinations and confidence.
        """
        sections = self.parse_response(response_text)

        # 1. Check for required sections
        required_sections = ["Thinking", "Fact Check", "Confidence Score", "Answer"]
        for section in required_sections:
            if section not in sections:
                return ScreeningResult(
                    passed=False,
                    confidence_score=0.0,
                    reason=f"Missing required section: [{section}]"
                )

        # 2. Check content not empty
        if not sections["Thinking"] or len(sections["Thinking"]) < 10:
             return ScreeningResult(
                passed=False,
                confidence_score=0.0,
                reason="Thinking process is too short or empty."
            )

        # 3. Parse and check Confidence Score
        try:
            score_text = sections["Confidence Score"]
            # Extract number from text (e.g., "85" or "Score: 85")
            score_match = re.search(r"(\d+)", score_text)
            if score_match:
                score = float(score_match.group(1))
            else:
                 return ScreeningResult(
                    passed=False,
                    confidence_score=0.0,
                    reason="Could not parse confidence score number."
                )
        except Exception as e:
            return ScreeningResult(
                passed=False,
                confidence_score=0.0,
                reason=f"Error parsing confidence score: {str(e)}"
            )

        if score < self.confidence_threshold:
            return ScreeningResult(
                passed=False,
                confidence_score=score,
                reason=f"Confidence score {score} is below threshold {self.confidence_threshold}."
            )

        # 4. Success
        return ScreeningResult(
            passed=True,
            confidence_score=score,
            reason="Passed all checks.",
            filtered_response=sections["Answer"] # Return only the clean answer
        )
