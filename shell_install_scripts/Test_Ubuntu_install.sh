#!/bin/bash

# Check if the script is running on Linux
if [ "$(uname)" == "Linux" ]; then

    # Update package lists
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install -y git
    sudo apt-get install -y calibre
    sudo apt-get install -y espeak
    sudo apt-get install -y espeak-ng
    sudo apt-get install -y ffmpeg
    sudo apt-get install -y curl
    sudo apt-get install -y zip
    sudo apt-get install -y unzip

    # Check for and install pip if needed
    if ! command -v pip &> /dev/null; then
        sudo apt-get install -y python3-pip
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

    # Clone the VoxNovel repository
    git clone https://github.com/DrewThomasson/VoxNovel.git

    # Navigate to the VoxNovel directory
    cd VoxNovel

    # Install necessary Python packages
    pip install styletts2 
    pip install tts==0.21.3
    pip install booknlp==1.0.7.1
    pip install bs4
    pip install -r Ubuntu_requirements.txt
    pip install ebooklib==0.18
    pip install epub2txt==0.1.6
    pip install pygame==2.6.0
    pip install moviepy==1.0.3

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

    # Step to automatically copy the nltk folder
    # Assume nltk.zip is placed in the home directory or a specified location
    USERNAME=$(whoami)
    FILESYSTEM_PATH="/home/$USERNAME/miniconda/envs/VoxNovel/lib/python3.10/site-packages/nltk"
    # Check if the path exists
    if [ -d "$FILESYSTEM_PATH" ]; then
        echo "Navigating to $FILESYSTEM_PATH"
    
        # Download the NLTK zip file
        wget https://github.com/user-attachments/files/16650539/nltk.zip -O /tmp/nltk.zip
        sudo apt-get update
        sudo apt-get install unzip -y
    
        # Unzip the file to a temporary directory
        unzip /tmp/nltk.zip -d /tmp/new_nltk
    
        # Replace the existing NLTK folder with the new one
        cp -r /tmp/new_nltk/nltk/* "$FILESYSTEM_PATH"
    
        # Clean up the temporary files
        rm -rf /tmp/nltk.zip /tmp/new_nltk
    
        echo "NLTK files have been successfully replaced."

else
    echo "This script is intended to be run on Linux."
fi
