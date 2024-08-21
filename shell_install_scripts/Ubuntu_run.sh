#!/bin/bash

# Activate the Conda environment
source /home/drew/miniconda/etc/profile.d/conda.sh
conda activate VoxNovel

# Navigate to the VoxNovel directory
cd ~/VoxNovel

# Run the Python script
python gui_run.py
