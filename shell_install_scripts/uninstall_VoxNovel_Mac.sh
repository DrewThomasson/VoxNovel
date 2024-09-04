#!/bin/bash

# Function to convert available storage to a comparable format (KB)
get_available_storage() {
    df / | tail -1 | awk '{print $4}'
}

# Get the available storage at the start
start_storage=$(get_available_storage)

# Calculate total storage to be reclaimed
total_storage_reclaimed="7.82 GB"

# Prompt user for confirmation
echo "This script will remove the following and reclaim approximately $total_storage_reclaimed of space:"
echo "- Conda environment 'VoxNovel' (around 4 GB)"
echo "- Brew Ffmpeg (around 51.8 MB)"
echo "- Brew Calibre (around 835 MB)"
echo "- nltk_data (around 44.9 MB)"
echo "- BookNLP models (around 1.2 GB)"
echo "- Xtts TTS model (around 1.7 GB)"
echo "- VoxNovel.app from Applications and Desktop"

read -p "Do you want to proceed? (y/n): " confirm

if [[ "$confirm" != "y" ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Uninstall Brew packages
brew uninstall --force ffmpeg calibre

# Delete specific folders
rm -rf "$HOME/nltk_data"
rm -rf "$HOME/booknlp_models"
rm -rf "$HOME/Library/Application Support/tts/tts_models--multilingual--multi-dataset--xtts_v2"

# Remove Conda environment
conda remove --name VoxNovel --all -y

# Delete VoxNovel.app from Applications and Desktop
rm -rf "/Applications/VoxNovel.app"
rm -rf "$HOME/Desktop/VoxNovel.app"

# Get the available storage at the end
end_storage=$(get_available_storage)

# Calculate the difference in available storage (KB to MB conversion)
storage_diff=$(( (end_storage - start_storage) / 1024 ))

# Display the amount of space reclaimed
echo "You have successfully reclaimed approximately $total_storage_reclaimed of space."
echo "Actual reclaimed space: $storage_diff MB."
