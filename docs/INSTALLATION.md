# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended)
- 5GB disk space for model storage

## Supported Platforms

- Linux (Ubuntu 20.04+, Debian 11+, Fedora 35+, Arch)
- macOS (10.15+)
- Windows (WSL2 recommended)

## Quick Install

```bash
git clone https://github.com/Mogalina/orcas.git
cd orcas
./scripts/install.sh
```

The installer will:
1. Create a virtual environment
2. Install all dependencies
3. Set up configuration files
4. Optionally download a model
5. Add shell integration

## Manual Installation

If you prefer manual installation:

### 1. Clone Repository

```bash
git clone https://github.com/Mogalina/orcas.git
cd orcas
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 4. Download Model

```bash
python scripts/download_model.py
```

Or manually download from Hugging Face:
- [GemmaCoder3-12B GGUF](https://huggingface.co/burtenshaw/GemmaCoder3-12B)
- [Phi-2 GGUF](https://huggingface.co/TheBloke/phi-2-GGUF)
- [TinyLlama GGUF](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)

Place the `.gguf` file in `~/.orcas/models/`

### 5. Create Configuration

```bash
mkdir -p ~/.config/orcas
cp config/default_config.yaml ~/.config/orcas/config.yaml
```

## GPU Acceleration (Optional)

For CUDA support:

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

Update config:
```yaml
model:
  n_gpu_layers: -1  # Use all GPU layers
```

## Verification

Test your installation:

```bash
orcas --version
orcas list files in current directory
```

## Troubleshooting

### "Model not found" Error

Download a model:
```bash
orcas --download-model
```

### Import Errors

Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Permission Issues

Ensure scripts are executable:
```bash
chmod +x scripts/*.sh
```

## Updating

```bash
cd orcas
git pull
pip install -e . --upgrade
```

## Uninstallation

```bash
pip uninstall orcas-cli
rm -rf ~/.orcas
rm -rf ~/.config/orcas
```

Remove shell aliases from `.bashrc` or `.zshrc`.
