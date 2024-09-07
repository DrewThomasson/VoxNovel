#!/bin/bash
echo "Starting..."
echo "Activating brew..." && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" && echo Activated Brew! launching VoxNovel..." && cd ~ && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" && conda activate VoxNovel && cd VoxNovel && git pull && python --version && python run gui_run.py && xdg-open ~/VoxNovel/output_audiobooks/
