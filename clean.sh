#!/bin/bash

# Clean Python cache and build artifacts
# Useful for clearing bytecode cache when code changes aren't reflected

echo "🧹 Cleaning Python cache files..."

# Remove __pycache__ directories
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
echo "✓ Removed __pycache__ directories"

# Remove .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✓ Removed .pyc files"

# Remove pytest cache
rm -rf .pytest_cache 2>/dev/null
echo "✓ Removed .pytest_cache"

# Remove coverage data
rm -rf .coverage htmlcov 2>/dev/null
echo "✓ Removed coverage files"

# Remove build and dist directories
rm -rf build dist *.egg-info 2>/dev/null
echo "✓ Removed build artifacts"

echo ""
echo "✅ Cache cleaning complete!"
echo "You can now run: ollama-tweak-advanced"
echo ""
