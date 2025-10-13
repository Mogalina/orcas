import os
from pathlib import Path
from typing import Optional, Dict, Any
import sys

try:
    from llama_cpp import Llama
except ImportError:
    print("Error: llama-cpp-python is not installed")
    print("Install it with: pip install llama-cpp-python")
    sys.exit(1)


class ModelManager:
    """Manages local LLM loading and inference."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model: Optional[Llama] = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the LLM model from disk."""
        # Silence llama.cpp info and debug logs
        os.environ["LLAMA_LOG_LEVEL"] = "error"

        model_path = Path(os.path.expanduser(self.config['path']))
        model_name = self.config['name']

        possible_files = list(model_path.glob(f"*{model_name}*.gguf"))
        if not possible_files:
            raise FileNotFoundError(
                f"No model found matching '{model_name}' in {model_path}\n"
                f"Please download a model first with: orcas --download-model"
            )

        model_file = possible_files[0]

        try:
            # Suppress stderr noise during model load
            with open(os.devnull, "w") as devnull:
                old_stderr = sys.stderr
                sys.stderr = devnull
                try:
                    self.model = Llama(
                        model_path=str(model_file),
                        n_ctx=self.config.get("n_ctx", 2048),
                        n_gpu_layers=self.config.get("n_gpu_layers", 0),
                        verbose=False,
                    )
                finally:
                    sys.stderr = old_stderr
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        """Generate text from the model."""
        if not self.model:
            raise RuntimeError("Model not loaded")

        response = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=0.2,
            top_p=0.95,
            stop=["\n\n", "User:", "Human:"],
            echo=False,
        )

        return response['choices'][0]['text'].strip()