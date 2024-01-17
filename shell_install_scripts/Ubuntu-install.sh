#!/bin/bash

# Check if the script is running on Linux
if [ "$(uname)" == "Linux" ]; then

    # Update package lists
    sudo apt-get update
    sudo apt update
    sudo apt upgrade
    sudo apt install git
    sudo apt install calibre
    sudo apt install espeak
    sudo apt install espeak-ng
    sudo apt install ffmpeg

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
    # Add Conda to PATH
    export PATH="$HOME/miniconda/bin:$PATH"
    # Activate the base Conda environment
    source ~/miniconda/bin/activate
    conda init
    conda activate VoxNovel

    # Install Calibre
    sudo apt-get install calibre

    # Clone the VoxNovel repository
    git clone https://github.com/DrewThomasson/VoxNovel.git

    # Navigate to the VoxNovel directory
    cd VoxNovel

    # Install necessary Python packages
    pip install styletts2 
    pip install tts==0.21.3
    pip install booknlp
    pip install bs4
    pip install -r Ubuntu_requirements.txt

    # Download the spaCy language model
    pip install spacy
    python -m spacy download en_core_web_sm



    # Create a Desktop Entry for the VoxNovel app
    echo "[Desktop Entry]
    Version=1.0
    Type=Application
    Name=VoxNovel
    Exec=$HOME/VoxNovel/shell_install_scripts/run/Ubuntu_run_voxnovel.sh
    Icon=$HOME/VoxNovel/readme_files/logo.jpeg
    Terminal=true
    " > $HOME/Desktop/VoxNovel.desktop
    cp $HOME/Desktop/VoxNovel.desktop ~/.local/share/applications
    
    # Make both Desktop Entries executable
    chmod +x $HOME/Desktop/VoxNovel.desktop
    chmod +x ~/.local/share/applications/VoxNovel.desktop
    # Make the Ubuntu voxnovel run script executable
    chmod +x $HOME/VoxNovel/shell_install_scripts/run/Ubuntu_run_voxnovel.sh
    # Update the application database
    sudo update-desktop-database

    
else
    echo "This script is intended to be run on Linux."
fi
