#!/bin/bash
# CloudPedagogy Quarto Course Generator - Build Script
# Usage: ./tools/build.sh [config_path]

CONFIG=${1:-config/epm102.yml}

# Ensure we are in the project root
cd "$(dirname "$0")/.."

echo "------------------------------------------------"
echo "🚀 CloudPedagogy Multi-Module Builder"
echo "------------------------------------------------"

echo "Step 1: Validating configuration ($CONFIG)..."
PYTHONPATH=src python3 -m course_generator.cli validate "$CONFIG" || exit 1

# Extract module code to determine paths
MODULE_ID=$(PYTHONPATH=src python3 -m course_generator.cli inspect "$CONFIG" | grep "Module:" | awk '{print $2}' | tr '[:upper:]' '[:lower:]')

if [ -z "$MODULE_ID" ]; then
    echo "Error: Could not identify Module Code from $CONFIG"
    exit 1
fi

SOURCE_DIR="course/$MODULE_ID"
SITE_DIR="output/$MODULE_ID/site"

echo "Step 2: Building Quarto scaffold into '$SOURCE_DIR'..."
PYTHONPATH=src python3 -m course_generator.cli build "$CONFIG" --force || exit 1

echo "Step 3: Rendering website into '$SITE_DIR'..."
mkdir -p "output/$MODULE_ID"
quarto render "$SOURCE_DIR" --output-dir "../../output/$MODULE_ID/site" || exit 1

echo "------------------------------------------------"
echo "✅ Done! Module '$MODULE_ID' is ready."
echo "Source: $SOURCE_DIR"
echo "Website: $SITE_DIR"
echo "------------------------------------------------"
