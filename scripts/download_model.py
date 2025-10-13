#!/usr/bin/env python3

import sys
import urllib.request
from pathlib import Path

MODELS = {
    "gemma-3": {
        "url": "https://huggingface.co/burtenshaw/gemma-3-12b-it-codeforces-SFT-Q4_K_M-GGUF/resolve/main/gemma-3-12b-it-codeforces-sft-q4_k_m.gguf",
        "filename": "gemma-3-12b-it-codeforces-sft-q4_k_m.gguf",
        "size": "7.3GB"
    },
    "phi-2": {
        "url": "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf",
        "filename": "phi-2.Q4_K_M.gguf",
        "size": "2.7GB"
    },
    "tinyllama": {
        "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "size": "1.1GB"
    }
}


def download_file(url: str, destination: Path) -> None:
    def report_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(downloaded / total_size * 100, 100)
        bar_length = 50
        filled_length = int(bar_length * downloaded / total_size)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f'\r|{bar}| {percent:.1f}%')
        sys.stdout.flush()

    print(f"Downloading to {destination}...")
    urllib.request.urlretrieve(url, destination, report_progress)
    print("\n✓ Download complete!")


def main() -> None:
    model_dir = Path.home() / ".orcas" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    print("\nAvailable models:")
    for i, (name, info) in enumerate(MODELS.items(), 1):
        print(f"  {i}. {name} ({info['size']})")

    choice = input(f"\nSelect a model (1-{len(MODELS.items())}) [1]: ").strip() or "1"

    try:
        model_name = list(MODELS.keys())[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice. Defaulting to gemma-3.")
        model_name = "gemma-3"

    model_info = MODELS[model_name]
    destination = model_dir / model_info["filename"]

    if destination.exists():
        print(f"\n    Model already exists at {destination}")
        overwrite = input("Overwrite? [y/N]: ").strip().lower()
        if overwrite != 'y':
            print("Download cancelled.")
            return

    try:
        download_file(model_info["url"], destination)
        print(f"\n✓ Model saved to: {destination}")
    except Exception as e:
        print(f"\n✗ Error downloading model: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
