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

# Adding homebrew to Konsol terminal bash profile
echo "Adding homebrew to Bash profile..."
echo 'if [ $(basename $(printf "%s" "$(ps -p $(ps -p $$ -o ppid=) -o cmd=)" | cut --delimiter " " --fields 1)) = konsole ] ; then '$'\n''eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"'$'\n''fi'$'\n' >> ~/.bash_profile
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.zshrc 
source ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

echo "Added homebrew to Bash profile!"

#For More info use follow this guide for installing homebrew on the SteamDeck
#https://gist.github.com/uyjulian/105397c59e95f79f488297bb08c39146

# Check if Miniconda is installed by checking if conda command is recognized
if ! command -v conda &> /dev/null
then
    echo "Miniconda not found."
    read -p "Would you like to install Miniconda? (y/n): " choice
    
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        echo "Installing Miniconda using the Arch Miniconda installer script..."
        
        # Use the one-liner to download and run the Miniconda installer script from GitHub
        bash <(curl -s https://raw.githubusercontent.com/DrewThomasson/WSL-scripts/main/Arch/arch-miniconda-installer.sh)

        # Initialize conda for bash and zsh (if required)
        if [ -f ~/miniconda3/bin/conda ]; then
            echo "Initializing Conda for bash and zsh..."
            ~/miniconda3/bin/conda init bash
            ~/miniconda3/bin/conda init zsh
        else
            echo "Error: Miniconda installation failed or path incorrect."
            exit 1
        fi
        
        # Source the shell to make conda available in this session
        echo "Reloading shell configuration..."
        source ~/.bash_profile || source ~/.bashrc
        source ~/.zshrc
        
        echo "Miniconda installation completed."
    else
        echo "Miniconda installation skipped. VoxNovel requires Miniconda to run. Exiting install script..."
        exit 1
    fi
else
    echo "Miniconda is already installed."
fi

# Step 5: Initialize Conda for bash and zsh
echo "Initializing Conda..."
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

# Step 6: Reload shell configuration
echo "Reloading shell configuration..."
source ~/.bashrc
source ~/.zshrc

echo "listing current existing conda envs"
conda env list


# Install necessary packages with Homebrew
echo "Installing Calibre, ffmpeg, git, espeak-ng, glibc, gcc, unzip, wget"
#brew install calibre
# installing calibre with the discover store instead becuase casks are only for mac
#sudo pkcon install calibre -y
# To uninstall with pkcon use the 'remove' modifer like pkcon remove calibre
#NOPE turns out for steam deck i gota use this command instead?
#flatpak install --system flathub com.calibre_ebook.calibre -y
#MY DUDE I COULD OF JUST USED THIS so much easier
sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin
#uninstall with this command 'sudo calibre-uninstall'
brew install ffmpeg
brew install git
brew install espeak-ng
brew install glibc 
brew install gcc
brew install unzip
brew install wget


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

# Download Spacy model
pip install spacy
python -m spacy download en_core_web_sm




# This will use the backup of the nltk files instead
echo "Replacing the nltk folder with the nltk folder backup I Pulled from a docker image, just in case the nltk servers ever mess up..."

# Variables
ZIP_URL="https://github.com/DrewThomasson/VoxNovel/blob/main/readme_files/nltk.zip?raw=true"
TARGET_DIR="$HOME/miniconda3/envs/VoxNovel/lib/python3.10/site-packages"
TEMP_DIR=$(mktemp -d)
    
# Download the zip file
echo "Downloading zip file..."
wget -q -O "$TEMP_DIR/nltk.zip" "$ZIP_URL"
    
# Extract the zip file
echo "Extracting zip file..."
unzip -q "$TEMP_DIR/nltk.zip" -d "$TEMP_DIR"
    
# Replace contents
echo "Replacing contents..."
rm -rf "$TARGET_DIR/nltk"
mv "$TEMP_DIR/nltk" "$TARGET_DIR/nltk"
    
# Clean up
echo "Cleaning up..."
rm -rf "$TEMP_DIR"
    
echo "NLTK Files Replacement complete."





# This part of the script will pre-download the tos_agreed.txt file so then you don't have to type yes in the terminal when downloading the coqio xtts_v2 model. 
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
echo "The tos_agreed.txt file is so that you don't have to tell coqio tts yes when downloading the xtts_v2 model."





# Create a Desktop Entry for the VoxNovel app on the Steam Deck
echo "[Desktop Entry]
Version=1.0
Type=Application
Name=VoxNovel
Exec=$HOME/VoxNovel/shell_install_scripts/run/Steam-Deck-Run-VoxNovel.sh
Icon=$HOME/VoxNovel/readme_files/logo.jpeg
Terminal=true
" > $HOME/Desktop/VoxNovel.desktop

# Copy the Desktop Entry to the applications directory
cp $HOME/Desktop/VoxNovel.desktop ~/.local/share/applications

# Make both Desktop Entries executable
chmod +x $HOME/Desktop/VoxNovel.desktop
chmod +x ~/.local/share/applications/VoxNovel.desktop

# Make the Steam Deck run script executable
chmod +x $HOME/VoxNovel/shell_install_scripts/run/Steam-Deck-Run-VoxNovel.sh

# Update the application database (not necessary on Steam Deck but included for consistency)
sudo update-desktop-database



# Print completion message
echo "VoxNovel.app has been successfully placed on your desktop and in the Applications folder."
echo "You can manually delete the dektop shortcut if you want."







echo "VoxNovel Install FINISHED! (You can close out of this window now)"
