#!/bin/bash

# Get the current user's home directory
USER_HOME=$(eval echo ~${SUDO_USER:-$USER})

# Set the destination directory and file URL
DEST_DIR="$USER_HOME/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2"
FILE_URL="https://github.com/DrewThomasson/VoxNovel/raw/main/readme_files/tos_agreed.txt"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Download the file to the destination directory
curl -o "$DEST_DIR/tos_agreed.txt" "$FILE_URL"

echo "File has been saved to $DEST_DIR/tos_agreed.txt"
