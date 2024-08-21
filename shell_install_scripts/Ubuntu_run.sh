#!/bin/bash

# Activate the Conda environment
CONDA_PATH=$(dirname $(which conda))
source $CONDA_PATH/../etc/profile.d/conda.sh
conda activate VoxNovel

# Navigate to the VoxNovel directory
VENV_DIR=$(conda info --envs | grep VoxNovel | awk '{print $NF}')
cd $VENV_DIR

# Run the Python script
python gui_run.py
