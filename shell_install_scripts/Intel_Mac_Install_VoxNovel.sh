#!/bin/bash

# Estimate total storage required
total_storage_required="~7.89 GB"

# Inform the user about the installation details and estimated storage usage
echo "This script will install the following components for VoxNovel and will take up approximately $total_storage_required of storage:"
echo "- Homebrew (if not already installed)"
echo "- Miniconda (if not already installed)"
echo "- Calibre (around 835 MB)"
echo "- Ffmpeg (around 51.8 MB)"
echo "- Git (around 51.5 MB)"
echo "- Espeak-ng (around 12.5 MB)"
echo "- Conda environment 'VoxNovel' (around 4 GB)"
echo "- NLTK data (around 44.9 MB)"
echo "- BookNLP models (around 1.2 GB)"
echo "- Xtts TTS model (around 1.7 GB)"
echo "- VoxNovel.app shortcut (desktop and Applications folder)"

# Prompt user for confirmation
read -p "Do you want to proceed with the installation? (y/n): " confirm

if [[ "$confirm" != "y" ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo "Starting the installation..."







# Install Homebrew
echo "Installing/updating homebrew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Check if Miniconda is installed by checking if conda command is recognized
if ! command -v conda &> /dev/null
then
    echo "Miniconda not found."
    read -p "Would you like to install Miniconda? (y/n): " choice
    
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        echo "Installing Miniconda..."
        
        # Create directory for Miniconda installation
        mkdir -p ~/miniconda3
        
        # Download Miniconda installer
        curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
        
        # Install Miniconda
        bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
        
        # Remove the installer
        rm ~/miniconda3/miniconda.sh
        
        # Initialize conda for bash and zsh
        ~/miniconda3/bin/conda init bash
        ~/miniconda3/bin/conda init zsh
        
        # Source the shell to make conda available in this session
        source ~/.bash_profile
        source ~/.zshrc
        
        echo "Miniconda installation completed."
    else
        echo "Miniconda installation skipped. VoxNovel requires Miniconda to run. Exiting install script..."
        exit 1
    fi
else
    echo "Miniconda is already installed."
fi


# Install necessary packages with Homebrew
echo "Installing Calibre and ffmpeg"
brew install calibre
brew install ffmpeg
brew install git
brew install espeak-ng

# Create and activate the VoxNovel conda environment
conda create --name VoxNovel python=3.10 -y







#This part will attempt to actiate conda by finding the conda.sh file, so it won't depend on if miniconda is called miniconda3 or miniconda or something else,

# Define potential base directories
BASE_DIRS=("$HOME" "/opt" "/usr/local")

# Initialize a flag to track if Conda was found
CONDA_FOUND=false

# Loop through each base directory and look for conda.sh
for BASE_DIR in "${BASE_DIRS[@]}"; do
    if [ -f "$BASE_DIR/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$BASE_DIR/miniconda3/etc/profile.d/conda.sh"
        CONDA_FOUND=true
        break
    elif [ -f "$BASE_DIR/miniconda/etc/profile.d/conda.sh" ]; then
        source "$BASE_DIR/miniconda/etc/profile.d/conda.sh"
        CONDA_FOUND=true
        break
    elif [ -f "$BASE_DIR/anaconda3/etc/profile.d/conda.sh" ]; then
        source "$BASE_DIR/anaconda3/etc/profile.d/conda.sh"
        CONDA_FOUND=true
        break
    elif [ -f "$BASE_DIR/anaconda/etc/profile.d/conda.sh" ]; then
        source "$BASE_DIR/anaconda/etc/profile.d/conda.sh"
        CONDA_FOUND=true
        break
    fi
done

# Check if Conda was found and sourced
if [ "$CONDA_FOUND" = false ]; then
    echo "Conda initialization script not found. Please ensure Conda is installed."
    exit 1
fi

# Activate the VoxNovel environment
conda activate VoxNovel

# Verify the environment
which python  # This should show the path to the Python executable in the VoxNovel env
python --version  # This should show the Python version in the VoxNovel env








# Clone the VoxNovel repository and navigate to the directory
cd ~
git clone https://github.com/DrewThomasson/VoxNovel.git
cd VoxNovel

# Install Python packages
pip install styletts2
#pip install tts==0.21.3
# This is the updated pip install for tts becuase the original repo is dead sad face
pip install coqui-tts
pip install booknlp==1.0.7.1 
pip install transformers==4.30.0
pip install -r MAC-requirements.txt
pip install ebooklib bs4 epub2txt pygame moviepy spacy

# Download Spacy model
python -m spacy download en_core_web_sm



echo "Grabbing nltk data from backup online in case the nltk servers didnt't work right..."

# Set the target directory
TARGET_DIR="/Users/$(whoami)/nltk_data"

# Create the directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Download the zip file to a temporary location
TEMP_ZIP="/tmp/mac_nltk_data.zip"
curl -L -o "$TEMP_ZIP" "https://huggingface.co/drewThomasson/VoxNovel_WSL_ENV/resolve/main/mac_nltk_data.zip?download=true"

# Unzip the downloaded file to a temporary directory
TEMP_DIR="/tmp/mac_nltk_data"
unzip -o "$TEMP_ZIP" -d "$TEMP_DIR"

# Copy the contents to the target directory, replacing any existing files
cp -R "$TEMP_DIR/nltk_data/"* "$TARGET_DIR/"

# Clean up temporary files
rm -rf "$TEMP_ZIP" "$TEMP_DIR"

echo "nltk_data has been updated in $TARGET_DIR"





# This part of the script will pre-download the tos_agreed.txt file so then you don't have to type yes in the terminal when downloading the coqio xtts_v2 model.
# Get the current user's home directory
USER_HOME=$(eval echo ~${SUDO_USER:-$USER})

# Set the destination directory and file URL
#This dir is also where the xtts model files are stored, so if you ever want to remove them to save any space
DEST_DIR="$USER_HOME/Library/Application Support/tts/tts_models--multilingual--multi-dataset--xtts_v2"
FILE_URL="https://github.com/DrewThomasson/VoxNovel/raw/main/readme_files/tos_agreed.txt"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Download the file to the destination directory
curl -o "$DEST_DIR/tos_agreed.txt" "$FILE_URL"

echo "File has been saved to $DEST_DIR/tos_agreed.txt"
echo "The tos_agreed.txt file is so that you don't have to tell coqio tts yes when downloading the xtts_v2 model."








#This part here will put the VoxNovel uninstaller app in the applicaions folder

# Set variables
UNINSTALLER_URL="https://github.com/DrewThomasson/VoxNovel/raw/main/readme_files/VoxNovel_Mac_Uninstaller.zip"
UNZIP_DIR="$HOME/Downloads/VoxNovel_Uninstaller"
ZIP_FILE="$HOME/Downloads/VoxNovel_Mac_Uninstaller.zip"

# Download the VoxNovel Uninstaller zip file
echo "Downloading VoxNovel Uninstaller..."
curl -L $UNINSTALLER_URL -o "$ZIP_FILE"

# Unzip the file
echo "Unzipping the VoxNovel Uninstaller..."
mkdir -p $UNZIP_DIR
unzip "$ZIP_FILE" -d $UNZIP_DIR

# Move the Uninstaller to the Applications folder
echo "Moving VoxNovel Uninstaller to the Applications folder..."
mv "$UNZIP_DIR/VoxNovel Uninstaller.app" /Applications/

# Delete the zip file and the unzipped folder
echo "Cleaning up..."
rm -rf "$ZIP_FILE" "$UNZIP_DIR"

echo "Uninstaller created and moved to the Applications folder. Cleanup complete."










#This part right here will download the Desktop shortcut to your Desktop and put the shortcut in your Applications folder for easy access!

# Define the URL of the ZIP file
ZIP_URL="https://github.com/DrewThomasson/VoxNovel/raw/main/readme_files/VoxNovel.app.zip"

# Define the destination directories
DESKTOP_DIR="$HOME/Desktop"
APPLICATIONS_DIR="/Applications"

# Define the temporary download location
TEMP_ZIP="$DESKTOP_DIR/VoxNovel.app.zip"

# Download the ZIP file
curl -L -o "$TEMP_ZIP" "$ZIP_URL"

# Unzip the contents to the desktop
unzip -o "$TEMP_ZIP" -d "$DESKTOP_DIR"

# Copy the .app to the Applications folder
cp -R "$DESKTOP_DIR/VoxNovel.app" "$APPLICATIONS_DIR"

# Remove the temporary ZIP file
rm "$TEMP_ZIP"

# Print completion message
echo "VoxNovel.app has been successfully placed on your desktop and in the Applications folder."
echo "You can manually delete the dektop shortcut if you want."







echo "VoxNovel Install FINISHED! (You can close out of this window now)"

