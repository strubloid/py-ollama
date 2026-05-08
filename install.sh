#!/bin/bash

# Install script for Ollama Tweak Advanced
# This script installs all dependencies and sets up the project

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Ollama Tweak Advanced - Installation Script${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check Python version is 3.9+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo -e "${RED}✗ Error: Python 3.9 or higher is required${NC}"
    echo "Current version: ${PYTHON_VERSION}"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}✗ Error: pip3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ pip3 is available${NC}\n"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${YELLOW}→ Installing ollama-tweak-advanced...${NC}"
echo "  Project directory: ${SCRIPT_DIR}\n"

# Install the package with dev dependencies
cd "$SCRIPT_DIR"

# Try to install, handling the externally-managed-environment error
if pip3 install -e ".[dev]" 2>&1 | grep -q "externally-managed-environment"; then
    echo -e "${YELLOW}→ Creating virtual environment...${NC}"
    
    # Create venv
    python3 -m venv venv
    source venv/bin/activate
    
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo -e "${YELLOW}→ Installing dependencies in venv...${NC}\n"
    
    pip install --upgrade pip setuptools wheel
    pip install -e ".[dev]"
else
    pip3 install --upgrade pip setuptools wheel
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✓ Installation completed successfully!${NC}"
echo -e "${GREEN}================================================${NC}\n"

echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Run the tool:"
echo -e "     ${YELLOW}ollama-tweak-advanced${NC}"
echo ""
echo -e "  2. Run tests:"
echo -e "     ${YELLOW}pytest tests/ -v${NC}"
echo ""
echo -e "  3. Format code:"
echo -e "     ${YELLOW}black src/ tests/${NC}"
echo ""
echo -e "  4. Lint code:"
echo -e "     ${YELLOW}ruff check src/ tests/${NC}"
echo ""

# Check if ollama is installed
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}\n"
else
    echo -e "${YELLOW}⚠ Note: Ollama is not installed${NC}"
    echo -e "  Install from: https://ollama.ai\n"
fi

echo -e "${GREEN}Setup complete!${NC}\n"
