#!/usr/bin/env bash

# Super simple background remover using rembg CLI

INPUT="data/bama-bg-pic"
OUTPUT="data/bama-no-bg-pic"

# Check rembg is installed
if ! command -v rembg &> /dev/null; then
    echo "Error: rembg not found."
    echo "Run: pip install \"rembg[cpu,cli]\""
    exit 1
fi

# Check input folder exists
if [ ! -d "$INPUT" ]; then
    echo "Error: Folder not found → $INPUT"
    exit 1
fi

echo "Input  : $INPUT"
echo "Output : $OUTPUT (will be created if missing)"
echo ""

# The actual one-liner command
rembg p "$INPUT" "$OUTPUT"

echo ""
echo "Done! Transparent images are now in: $OUTPUT"
echo "Quick peek:"
ls -lh "$OUTPUT" | head -n 8