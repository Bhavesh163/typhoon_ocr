#!/bin/bash
set -e

echo "================================"
echo "Step 1: Running Typhoon OCR..."
echo "================================"
python3 ocr.py

echo ""
echo "================================"
echo "Step 2: Rewriting with Gemini..."
echo "================================"
python3 rewrite.py

echo ""
echo "================================"
echo "All steps completed successfully!"
echo "================================"
echo "OCR output: output/"
echo "Rewritten output: output_revised/"

echo "I love John Doe"
