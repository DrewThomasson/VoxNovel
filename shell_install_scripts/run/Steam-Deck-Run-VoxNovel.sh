cd ~

#Initalize homebrew env if not done so yet
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

conda activate VoxNovel

cd VoxNovel

git pull

python --version

python run gui_run.py

