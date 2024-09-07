# Just to be safe drew youll probbaly have to run all these at the beginning of the VoxNovel Launch script
# Activate nix Packages temporarily for the current session
echo "Activating Nix Packages..."

nix-shell -p calibre
nix-shell -p glibc
nix-shell -p gcc
nix-shell -p ffmpeg
nix-shell -p git
nix-shell -p espeak
nix-shell -p unzip
nix-shell -p wget

calibre --version
gcc --version
nix-shell -p glibc --run "ldd --version"
ffmpeg --version
git --version
espeak --version
unzip -v
wget --version


echo "Nix Packages Activated!"





echo "Activating Miniconda in current session..."

# Step 5: Initialize Conda for bash and zsh
echo "Initializing Conda..."
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

# Step 6: Reload shell configuration
echo "Reloading shell configuration..."
source ~/.bashrc
source ~/.zshrc

conda --version

echo "Miniconda Activated!"

cd ~
cd VoxNovel
git pull
conda activate VoxNovel
python --version
python run gui_run.py


echo "Opening output_audiobooks folder in xdg..."
xdg-open ~/VoxNovel/output_audiobooks/
echo "Opened! You can view your finished audiobooks here!"
echo "Complete!"


