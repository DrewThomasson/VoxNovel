# VoxNovel
![VoxNovelLogo](https://github.com/DrewThomasson/VoxNovel/assets/126999465/34b5b312-aa70-44e4-a35c-f3f5ac1b24de)


## Overview

VoxNovel is an innovative program that leverages the capabilities of booknlp to analyze literature, attribute quotations to specific characters, and generate a tailored audiobook where each character has a distinct voice through coqui tts. This not only provides an immersive audiobook experience but also brings each character to life with a unique voice, making the listening experience much more engaging.


   **DEMO**
   
 **High Quality Tortoise Demos**
 
https://github.com/DrewThomasson/VoxNovel/assets/126999465/c4f8dfdf-c5bd-4771-ab1a-6131c22a67b2

 **Super fast audio Balacoon Demos**
 
https://github.com/DrewThomasson/VoxNovel/assets/126999465/530e8781-c77c-4424-89cd-a02df363b0bf


https://github.com/DrewThomasson/VoxNovel/assets/126999465/53b694a9-5ddd-4174-82bc-07aff22d2330


# SetUp install

Run in this order:

if on Linux

`sudo apt-get install calibre`
1. `conda create --name VoxNovel python=3.10`
2. `conda activate VoxNovel`
3. `git clone https://github.com/DrewThomasson/VoxNovel.git`
4. `cd VoxNovel/VoxNovel+BookNLP\(FREE\)/coqui-tts/`
5. `pip install tts`
6. `pip install booknlp`
7. `pip install -r requirements.txt`

If on intel mac 

`brew install calibre`
1. `conda create --name VoxNovel python=3.10`
2. `conda activate VoxNovel`
3. `git clone https://github.com/DrewThomasson/VoxNovel.git`
4. `cd VoxNovel/VoxNovel+BookNLP\(FREE\)/coqui-tts/`
5. `pip install tts`
6. `pip install booknlp`
7.`pip install -r MAC-requirements.txt`

If on Windows

install calibre for windows
1. `conda create --name VoxNovel python=3.10`
2. `conda activate VoxNovel`
3. `git clone https://github.com/DrewThomasson/VoxNovel.git`
4. `cd VoxNovel/VoxNovel+BookNLP\(FREE\)/coqui-tts/`
5. `pip install tts`
6. `pip install booknlp`

7.`pip install -r Windows-requirements.txt`
```bash
# To Run the program
python gui_run.py


**To Run the program**
python gui_run.py

**To run the auto version here all you do is select the book and nothing else**

python auto_noGui_run.py

**folders**

Final_combined_output_audio:
-This is where all of your final audio files will be put in order of chapter num
