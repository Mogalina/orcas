#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🐋  Orcas Installation Script${NC}"

PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python is not installed${NC}"
    exit 1
fi

echo -e "\n${GREEN}✓${NC} Found Python $PYTHON_VERSION"

if ! $PYTHON_CMD -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}Error: Python 3.8 or higher is required${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Creating virtual environment...${NC}"
$PYTHON_CMD -m venv .venv
source .venv/bin/activate

echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

echo -e "\n${YELLOW}Installing Orcas...${NC}"
pip install -e .

CONFIG_DIR="$HOME/.config/orcas"
MODEL_DIR="$HOME/.orcas/models"
mkdir -p "$CONFIG_DIR"
mkdir -p "$MODEL_DIR"

if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
    echo -e "${YELLOW}Creating default configuration...${NC}"
    cp config/default_config.yaml "$CONFIG_DIR/config.yaml"
    echo -e "${GREEN}✓${NC} Config created at $CONFIG_DIR/config.yaml"
fi

echo -e "\n${YELLOW}Would you like to download the default model (Gemma3, ~7.3GB)? [y/N]${NC}"
read -r DOWNLOAD_MODEL

if [[ "$DOWNLOAD_MODEL" =~ ^[Yy]$ ]]; then
    $PYTHON_CMD scripts/download_model.py
else
    echo -e "Skipping model download. You can download it later with:"
    echo -e "  orcas --download-model"
fi

echo -e "\n${YELLOW}Setting up shell integration...${NC}"
SHELL_NAME=$(basename "$SHELL")
SHELL_RC=""

case "$SHELL_NAME" in
    bash)
        SHELL_RC="$HOME/.bashrc"
        ;;
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ;;
    fish)
        SHELL_RC="$HOME/.config/fish/config.fish"
        ;;
    *)
        echo -e "${YELLOW}Unknown shell: $SHELL_NAME${NC}"
        ;;
esac

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "# Orcas CLI" "$SHELL_RC" 2>/dev/null; then
        echo -e "\n# Orcas CLI" >> "$SHELL_RC"
        echo "alias orcas='source $(pwd)/.venv/bin/activate && orcas'" >> "$SHELL_RC"
        echo -e "${GREEN}✓${NC} Added alias to $SHELL_RC"
        echo -e "${YELLOW}Please run: source $SHELL_RC${NC}"
    fi
fi

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "\nTo get started:"
echo -e "  1. Activate the virtual environment: ${YELLOW}source .venv/bin/activate${NC}"
echo -e "  2. Run: ${YELLOW}orcas --help${NC}"
echo -e "  3. Try: ${YELLOW}orcas list all python files${NC}"
echo -e "\nFor more information, see docs/USAGE.md"