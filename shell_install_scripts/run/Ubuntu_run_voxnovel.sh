#!/bin/bash

# Iterate through common Miniconda paths
for miniconda_path in ~/miniconda ~/miniconda3 ~/opt/miniconda ~/opt/miniconda3 /opt/miniconda /opt/miniconda3; do
  if [[ -d $miniconda_path ]]; then
    source "$miniconda_path/bin/activate" VoxNovel
    break  # Exit the loop if a valid path is found
  fi
done

if [[ "$CONDA_PREFIX" == "" ]]; then
  echo "Error: Could not find Miniconda installation."
  exit 1
fi

cd ~/VoxNovel
git pull
python gui_run.py
