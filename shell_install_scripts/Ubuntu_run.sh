#!/bin/bash

echo "Conda path: $(which conda)"
echo "Available environments:"
conda env list

echo "Activating environment..."
source ~/miniconda/etc/profile.d/conda.sh
conda activate VoxNovel

echo "Current environment: $CONDA_DEFAULT_ENV"

cd ~/VoxNovel

echo "Running Python script..."
cd ~ && cd VoxNovel && python gui_run.py
