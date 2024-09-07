#!/bin/bash

# >>> conda initialize >>>
echo "Activating conda..."
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/drew/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/drew/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/drew/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/drew/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
echo "conda activated!"
# <<< conda initialize <<<

# Activate Homebrew
echo "Activating brew..."
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
echo "Brew activated!"

echo "Starting..."

# Change to home directory
cd ~

conda env list

# Activate Conda environment
conda activate VoxNovel

# Navigate to VoxNovel directory
cd VoxNovel

# Pull latest changes from the repository
git pull

# Display Python version
python --version

# Run the VoxNovel GUI
python gui_run.py && xdg-open ~/VoxNovel/output_audiobooks
