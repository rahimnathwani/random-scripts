#!/bin/bash

# Check if an input file was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input.mp3>"
    exit 1
fi

input_file="$1"

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' not found"
    exit 1
fi

# Check if input file is an MP3
if ! file "$input_file" | grep -i "mp3" > /dev/null; then
    echo "Error: Input file must be an MP3"
    exit 1
fi

# Check if required commands exist
for cmd in ffmpeg whisper-cli; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: Required command '$cmd' not found"
        exit 1
    fi
done

# Get the base name without extension
basename=$(basename "$input_file" .mp3)
dirname=$(dirname "$input_file")

# Create temporary directory
temp_dir=$(mktemp -d)
temp_wav="$temp_dir/temp.wav"

echo "Converting MP3 to WAV..."
if ! ffmpeg -i "$input_file" -ar 16000 -ac 1 -c:a pcm_s16le "$temp_wav" -y &> /dev/null; then
    echo "Error: Failed to convert MP3 to WAV"
    rm -rf "$temp_dir"
    exit 1
fi

echo "Running whisper..."
output_file="$dirname/$basename.txt"

if ! whisper-cli -m /Users/rahim/src/public/whisper.cpp/models/ggml-large-v3-turbo.bin -f "$temp_wav" > "$output_file"; then
    echo "Error: Whisper processing failed"
    rm -rf "$temp_dir"
    exit 1
fi

# Clean up
rm -rf "$temp_dir"

echo
echo "Successfully created transcription at: $output_file"
