from typing import Optional
import os
from dataclasses import dataclass

MODEL_TYPE = os.environ.get("MODEL_TYPE", "transformers")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt2")

@dataclass
class GenerationResult:
    text: str

class InferenceAdapter:
    def __init__(self):
        self.model_type = MODEL_TYPE
        self.model_name = MODEL_NAME
        self.pipe = None

    def generate(self, prompt: str, max_tokens: int = 64, temperature: float = 0.7) -> GenerationResult:
        return GenerationResult(text=prompt + " [Generated text placeholder]")

_adapter = None

def get_adapter():
    global _adapter
    if _adapter is None:
        _adapter = InferenceAdapter()
    return _adapter
