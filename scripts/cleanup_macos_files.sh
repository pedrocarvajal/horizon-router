#!/bin/bash

echo "Cleaning up macOS metadata files..."

# Remove problematic cache directories completely
rm -rf .mypy_cache 2>/dev/null || true
rm -rf __pycache__ 2>/dev/null || true

# Remove ._ files from root directory
rm -f ._* 2>/dev/null || true

# Remove .DS_Store files
find . -name ".DS_Store" -delete 2>/dev/null || true

# Remove ._ files recursively, excluding protected directories
find . -name "._*" \
    -not -path "./venv/*" \
    -not -path "./.git/*" \
    -not -path "./node_modules/*" \
    -type f -delete 2>/dev/null || true

# Remove __pycache__ directories
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Clear extended attributes from key files
for file in Dockerfile makefile docker-compose.yml docker-compose.override.yml docker-compose.prod.yml; do
    if [ -f "$file" ]; then
        xattr -c "$file" 2>/dev/null || true
    fi
done

# Clear extended attributes from root directory files only
find . -maxdepth 1 -type f -exec xattr -c {} \; 2>/dev/null || true

echo "Cleanup completed."
