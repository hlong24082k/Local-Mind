import os
import google.generativeai as genai

from typing import Optional, List
from dotenv import load_dotenv

from src.llm.base import LLMBase, LLMResponse  # assuming base.py defines LLMBase and LLMResponse


load_dotenv(".env", override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class GeminiProvider(LLMBase):
    """
    Gemini LLM provider implementation.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        :param api_key: Google Generative AI API key
        :param model_name: Gemini model name (e.g. "gemini-1.5-pro" or "gemini-1.5-flash")
        """
        super().__init__(provider_name="gemini")
        self.model_name = model_name
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.2,
        stop: Optional[List[str]] = None,
        stream: bool = False,
        **kwargs,
    ) -> LLMResponse:
        """
        Generate text using Gemini model.
        """
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        if stop:
            generation_config["stop_sequences"] = stop

        try:
            if stream:
                # Gemini supports streaming
                response_stream = self.model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    stream=True,
                    **kwargs,
                )
                text_output = ""
                for chunk in response_stream:
                    if chunk.candidates and chunk.candidates[0].content.parts:
                        text_output += chunk.candidates[0].content.parts[0].text
            else:
                response = self.model.generate_content(
                    prompt,
                    # generation_config=generation_config,
                    **kwargs,
                )
                text_output = response.text or ""
            
            return LLMResponse(
                text=text_output.strip(),
                provider=self.provider,
                metadata={
                    "model": self.model_name,
                },
            )
        except Exception as e:
            return LLMResponse(
                text=f"[Error] Gemini generation failed: {e}",
                provider=self.provider,
                metadata={"error": str(e)},
            )
