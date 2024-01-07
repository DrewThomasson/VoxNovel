# VoxNovel
![271860680-34b5b312-aa70-44e4-a35c-f3f5ac1b24de](https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/6d201a5b-c2b4-4931-991f-b2f927c173e7)



## Overview

VoxNovel is an innovative program that leverages the capabilities of booknlp to analyze literature, attribute quotations to specific characters, and generate a tailored audiobook where each character has a distinct voice through coqui tts. This not only provides an immersive audiobook experience but also brings each character to life with a unique voice, making the listening experience much more engaging.


### Supported ebook File Types: 
.epub, .pdf, .mobi, .txt, .html, .rtf, .chm, .lit, .pdb, .fb2, .odt, .cbr, .cbz, .prc, .lrf, .pml, .snb, .cbc, .rb, and .tcr,
(Best results are from using epub or mobi for auto chapter detection)

### outputs as a m4b with all book metadata and chapters, example output file in a audiobook player app
![IMG_FFAE40F23437-1](https://github.com/DrewThomasson/bark/assets/126999465/d3d53398-d06c-496f-bc25-317a9db44e26)
(as well as a folder of individual mp4 chatper files with book image if you want that)

   **DEMO**


 **High Quality XTTS V2 Demos**
 
https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/9e10b36d-b2e9-4462-8bad-13a3d8fce192


 **High Quality Tortoise Demos**
 
https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/94e23918-b7e1-4399-935e-179dd12212c3

 **Super fast audio Balacoon Demos**
 
https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/5e3c5501-4c87-462b-a11b-a15f546e51f4



https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/f4e57afe-53df-485c-81ff-65d7dcf29cb5

## GUI

<img width="168" alt="Screenshot 2023-11-26 at 10 37 54 PM" src="https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/6c6fae3c-b2c7-48bb-a066-6b06303baca5">
<img width="1201" alt="Screenshot 2024-01-07 at 2 27 18 AM" src="https://github.com/DrewThomasson/bark/assets/126999465/fe8eaf87-df32-4cf0-ba78-37aabb667ce2">
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

## If on Windows 11 (demo voice sounds not working in GUI yet due to WSL)

Because of BookNLP Windows issues, all of this will be run in WSL (don't worry, it's still easy).

1. In your PowerShell, paste `wsl --install` to install WSL.

2. After you set the username and password, you'll now be able to open WSL as an application. This will allow you to run Ubuntu software. You'll now want to open WSL if you closed it and paste these commands.

   (This will install Calibre for ebook conversion)
   `cd ~`
   `sudo apt update`
   `sudo apt upgrade`
   `sudo apt install calibre`

   (This will install Miniconda)
Mini conda code was taken from here:https://docs.conda.io/projects/miniconda/en/latest/
   `mkdir -p ~/miniconda3`
   `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh`
   `bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3`
   `rm -rf ~/miniconda3/miniconda.sh`

   (This will make sure Miniconda is initialized)
   `~/miniconda3/bin/conda init bash`
   `~/miniconda3/bin/conda init zsh`

3. Close out of your current WSL window and reopen it to be able to use Miniconda.

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

You can access the files on your WSL Ubuntu in Windows File Explorer by putting this into the address: `\\wsl.localhost\Ubuntu\home\`



##   To Run the program
`python gui_run.py`


##  To Run the auto program
This means all you do is select the book and all the voices will be auto assigned and generated for you.

`python auto_noGui_run.py`

**folders**

Final_combined_output_audio:
-This is where all of your final audio files will be put in order of chapter num

## Features
- Free and entirely locally run
- Supports all ebook file formats by using calibre
- Can run on CPU or CUDA GPU
- Autoselects a starting estimated voice by pronouns per character
- Supports all models in Coqui TTS and all voices in the models
- Easily create a new voice actor in seconds through voice cloning in GUI
- Can play audio by clicking on the text in the book viewer in GUI
- Ability to regenerate specific lines if they came out weird
- Ability to add custome fine tuned models for specific voice with the click of a button in GUI
- Outputs a single file output as m4b to include all the metadata(chapters book image ect)




## Incoming Planned Features
- Ability to change the character for a line if incorrectly attributed by booknlp
- Make it so that all the included voices and models already have their premade own demo voices
- Make it so that the demo audio for the cloned voices is not their reference audio but what their voices sound like generated
- Using whisper transcriptions to cut hallucinations out of generated audio





