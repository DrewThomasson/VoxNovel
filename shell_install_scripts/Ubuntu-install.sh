#!/bin/bash

# Check if the script is running on Linux
if [ "$(uname)" == "Linux" ]; then

    # Update package lists
    sudo apt-get update
    sudo apt update
    sudo apt install git

    # Check for and install pip if needed
    if ! command -v pip &> /dev/null; then
        sudo apt-get install python3-pip
    fi

    # Check for Python 3.10 or later and install if needed
    python_version=$(python3 --version 2>&1)
    if [[ ! "$python_version" =~ ^Python\ (3\.1[0-9]|3\.[2-9]\.|[4-9]\.) ]]; then
        sudo apt-get install python3.10
    fi

    # Check for Conda and install if needed
    if ! command -v conda &> /dev/null; then
        # Download and install Miniconda
        miniconda_installer="Miniconda3-latest-Linux-x86_64.sh"
        wget https://repo.anaconda.com/miniconda/$miniconda_installer
        bash $miniconda_installer -b -p ~/miniconda
        rm $miniconda_installer
        # Add Conda to PATH
        export PATH="$HOME/miniconda/bin:$PATH"
    fi

    # Create and activate a new Conda environment using Python 3.10
    conda create --name VoxNovel python=3.10
    conda init
    conda activate VoxNovel

    # Install Calibre
    sudo apt-get install calibre

    # Clone the VoxNovel repository
    git clone https://github.com/DrewThomasson/VoxNovel.git

    # Navigate to the VoxNovel directory
    cd VoxNovel

    # Install necessary Python packages
    pip install styletts2 tts==0.21.3 booknlp
    pip install -r Ubuntu_requirements.txt

    # Download the spaCy language model
    python -m spacy download en_core_web_sm
else
    echo "This script is intended to be run on Linux."
fi
