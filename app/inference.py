from typing import Optional
import os
from dataclasses import dataclass
from transformers import pipeline

MODEL_TYPE = os.environ.get("MODEL_TYPE", "transformers")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt2")

@dataclass
class GenerationResult:
    text: str

class InferenceAdapter:
    def __init__(self):
        self.model_type = MODEL_TYPE
        self.model_name = MODEL_NAME
        # This line initializes the model pipeline. It runs only once.
        print(f"Loading model: {self.model_name}")
        # device=-1 tells transformers to use the CPU.
        self.pipe = pipeline("text-generation", model=self.model_name, device=-1)
        print("Model loaded successfully.")

    def generate(self, prompt: str, max_tokens: int = 64, temperature: float = 0.7) -> GenerationResult:
        # The pipeline returns a list of dictionaries; we want the text from the first one.
        results = self.pipe(prompt, max_new_tokens=max_tokens, temperature=temperature, do_sample=True)
        generated_text = results[0]['generated_text']
        return GenerationResult(text=generated_text)

_adapter = None

def get_adapter():
    global _adapter
    if _adapter is None:
        _adapter = InferenceAdapter() # Create the adapter instance if it doesn't exist
    return _adapter