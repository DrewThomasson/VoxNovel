#!/bin/bash

# Check if the script is running on Linux
if [ "$(uname)" == "Linux" ]; then
    # Update package lists and install Calibre
    sudo apt-get update
    sudo apt-get install calibre

    # Create and activate a new Conda environment
    conda create --name VoxNovel python=3.10
    conda activate VoxNovel

    # Clone the VoxNovel repository
    git clone https://github.com/DrewThomasson/VoxNovel.git

    # Navigate to the VoxNovel directory
    cd VoxNovel

    # Install necessary Python packages
    pip install styletts2
    pip install tts==0.21.3
    pip install booknlp
    pip install -r Ubuntu_requirements.txt

    # Download the spaCy language model
    python -m spacy download en_core_web_sm
else
    echo "This script is intended to be run on Linux."
fi
