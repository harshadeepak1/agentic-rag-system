"""
Local LLM interface using HuggingFace pipeline
(Stable replacement for Gemini)
"""

from transformers import pipeline
from typing import List, Dict, Optional
from utils.logger import logger


class LLMInterface:
    def __init__(self):
        logger.info("Loading local LLM (distilgpt2)...")

        self.generator = pipeline(
            "text-generation",
            model="distilgpt2",
            max_new_tokens=150
        )

        logger.info("Local LLM ready")

    def generate(self, prompt: str, temperature=0.7, max_tokens=512) -> str:
        try:
            result = self.generator(prompt)[0]["generated_text"]
            return result
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return "Generation failed."

    def generate_answer(
        self,
        query: str,
        context: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:

        context_str = "\n\n".join([
            chunk["text"] for chunk in context
        ])

        prompt = f"""
Context:
{context_str}

Question:
{query}

Answer:
"""

        return self.generate(prompt)

    def classify_query(self, query: str, categories: List[str]) -> str:
        return categories[0]

    def extract_keywords(self, text: str, max_keywords=5):
        return text.split()[:max_keywords]


llm = LLMInterface()
