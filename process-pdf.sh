#!/bin/bash

# Check if a filename was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <pdf-file>"
    exit 1
fi

# Convert to absolute paths
input_pdf=$(realpath "$1")
original_dir=$(dirname "$input_pdf")

# Check if input file exists
if [ ! -f "$input_pdf" ]; then
    echo "Error: File '$input_pdf' not found"
    exit 1
fi

# Create temporary directory
temp_dir=$(mktemp -d)
if [ $? -ne 0 ]; then
    echo "Error: Failed to create temporary directory"
    exit 1
fi

# Clean up temp directory on script exit
trap 'rm -rf "$temp_dir"' EXIT

# Extract base name and extension
base_name=$(basename "${input_pdf%.*}")
extension="${input_pdf##*.}"
output_pdf="$original_dir/${base_name}-bw.${extension}"

echo "Processing $input_pdf..."

# Change to temp directory and extract PNG files from PDF
cd "$temp_dir" && mutool extract "$input_pdf"
if [ $? -ne 0 ]; then
    echo "Error: Failed to extract images from PDF"
    exit 1
fi

# Keep only grayscale PNGs
for png in *.png; do
    if [ -f "$png" ]; then
        # Check if image is sRGB using ImageMagick's identify
        if identify -verbose "$png" | grep -q "Colorspace: sRGB"; then
            echo "Removing sRGB image: $png"
            rm "$png"
        else
            echo "Keeping grayscale image: $png"
        fi
    fi
done

# Check if we have any PNG files left
png_count=$(ls -1 *.png 2>/dev/null | wc -l)
if [ "$png_count" -eq 0 ]; then
    echo "Error: No grayscale PNG files found"
    exit 1
fi

# Convert remaining PNGs to PDF with negation
convert *.png -negate "$output_pdf"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create output PDF"
    exit 1
fi

echo "Successfully created: $output_pdf"
