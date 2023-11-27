# VoxNovel
![271860680-34b5b312-aa70-44e4-a35c-f3f5ac1b24de](https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/6d201a5b-c2b4-4931-991f-b2f927c173e7)



## Overview

VoxNovel is an innovative program that leverages the capabilities of booknlp to analyze literature, attribute quotations to specific characters, and generate a tailored audiobook where each character has a distinct voice through coqui tts. This not only provides an immersive audiobook experience but also brings each character to life with a unique voice, making the listening experience much more engaging.


   **DEMO**
   
 **High Quality Tortoise Demos**
 
https://github.com/DrewThomasson/VoxNovel/assets/126999465/c4f8dfdf-c5bd-4771-ab1a-6131c22a67b2

 **Super fast audio Balacoon Demos**
 
https://github.com/DrewThomasson/VoxNovel/assets/126999465/530e8781-c77c-4424-89cd-a02df363b0bf


https://github.com/DrewThomasson/VoxNovel/assets/126999465/53b694a9-5ddd-4174-82bc-07aff22d2330

## GUI

<img width="168" alt="Screenshot 2023-11-26 at 10 37 54 PM" src="https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/6c6fae3c-b2c7-48bb-a066-6b06303baca5">
<img width="1199" alt="Screenshot 2023-11-26 at 10 38 31 PM" src="https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/c2aeff6f-78b8-478a-8369-bb089862236b">
<img width="585" alt="Screenshot 2023-11-26 at 10 35 39 PM" src="https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/5b2c473c-7806-40c0-931a-091306de347d">


# SetUp install

Run in this order:

##  if on Linux

1. `sudo apt-get install calibre`
2. `conda create --name VoxNovel python=3.10`
3. `conda activate VoxNovel`
4. `git clone https://github.com/DrewThomasson/VoxNovel.git`
5. `cd VoxNovel`
6. `pip install tts`
7. `pip install booknlp`
8. `pip install -r Ubuntu_requirements.txt`
9. `python -m spacy download en_core_web_sm`


##  if on Steam Deck) (x86_64 Arch Linux)

1. `sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin`
2. `also download it from the discovery store or flatpac I did both on my steam deck`
3. `mkdir -p ~/miniconda3`
4. `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh`
5. `bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3`
6. `rm -rf ~/miniconda3/miniconda.sh`
7. `~/miniconda3/bin/conda init bash`
8. `~/miniconda3/bin/conda init zsh`
9. `restart the terminal(close out and open a new window)`
10. `conda create --name VoxNovel python=3.10`
11. `conda activate VoxNovel`
12. `git clone https://github.com/DrewThomasson/VoxNovel.git`
13. `cd VoxNovel`
14. `sudo pacman -S espeak-ng`(make sure you have pacman fully working, there should be stuff online for the steam deck)
guide on getting pacman wokring on steam deck(https://www.reddit.com/r/SteamDeck/comments/t8al0i/install_arch_packages_on_your_steam_deck/)
you might have to reset the keys if something goes wrong with that: Resetting all the keys

Remove or reset all the keys installed in your system by removing the /etc/pacman.d/gnupg directory (as root) and by rerunning pacman-key --init followed by pacman-key --populate to re-add the default keys. 
15. `pip install tts`
16. `pip install booknlp`
17. `pip install -r SteamDeck_requirements.txt`
18. `pip3 install spacy`
19. `python3 -m spacy download en_core_web_sm`
20. `sudo pacman -S calibre`
21. mv ~/miniconda3/envs/VoxNovel/lib/libstdc++.so.6 ~/miniconda3/envs/tts/lib/libstdc++.so.6.bak

22. `pip install mechanize`
23. `pip install bs4`
24. `pip install css_parser`

##  If on intel mac 

1. `brew install calibre`
2. `conda create --name VoxNovel python=3.10`
3. `conda activate VoxNovel`
4. `git clone https://github.com/DrewThomasson/VoxNovel.git`
5. `cd VoxNovel`
6. `pip install tts`
7. `pip install booknlp`
8.`pip install -r MAC-requirements.txt`
9. `pip spacy`
10.`python -m spacy download en_core_web_sm`

##  If on Windows 11(demo voice sounds not working in gui yet cause wsl)
So becuase of booknlp windows issues all of this will be run in wsl(don't worry its still easy)
1. In your powershell paste `wsl --install` to install wsl
2. After you set the username and password you'll now be able to open wsl as a application this will allow you to run ubuntu software
You'll now want to open wsl if you closed it and paste these commands
(This will install calibre for ebook conversion)
`cd ~`
`sudo apt update`
`sudo apt upgrade`
`sudo apt install calibre`
(This will install miniconda)
`mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh`
(This will make sure miniconda is initalized)
`~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh`
3. Close out of your current wsl window and reopen it to be able to use miniconda
`conda create --name VoxNovel python=3.10`
`conda activate VoxNovel`
`cd ~`
`git clone https://github.com/DrewThomasson/VoxNovel.git`
`cd VoxNovel`
`pip install tts`
`pip install booknlp`
`pip install -r Ubuntu-requirements.txt`
`pip install spacy`
`python -m spacy download en_core_web_sm`
`sudo apt install espeak-ng`
You can acess the files on your wsl ubuntu in windows file exploror by putting this into the address
`\\wsl.localhost\Ubuntu\home\`


##   To Run the program
`python gui_run.py`


##  To Run the auto program
This means all you do is select the book and all the voices will be auto assigned and generated for you.

`python auto_noGui_run.py`

**folders**

Final_combined_output_audio:
-This is where all of your final audio files will be put in order of chapter num


## features
-free and entirly locally run
-supports all ebook file formats by using calibre
-can run on cpu or cuda gpu
-autoselects a starting estimated voice by pronouns per character
-supports all models in Coqui TTS and all voices in the models
-easily create a new voice actor in seconds through voice cloneing in gui
-can play audio by clicking on the text in the book viewer in gui
-Ability to regenerate specific lines if they came out weird



## incoming planned features
-Ability to change the character for a line if incorectly attributed by booknlp
-Ability to regenerate specific lines
-Make it so that all the included voices and models already have their premade own demo voices
-Make it so that the demo audio for the cloned voices is the not their refrence audio but what their voices sound like generated
-Using whisper transcriptions to cut hallucinations out of generated audio




