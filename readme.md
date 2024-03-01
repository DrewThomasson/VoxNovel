# VoxNovel
![Voxnovel_Logo](https://github.com/DrewThomasson/VoxNovel/blob/6f49c6a8b36927c987b1d628ff3e9c1afcb04dab/readme_files/logo.jpeg)



## 📋 Overview

VoxNovel is an innovative program that leverages the capabilities of booknlp to analyze literature, attribute quotations to specific characters, and generate a tailored audiobook where each character has a distinct voice through coqui tts. This not only provides an immersive audiobook experience but also brings each character to life with a unique voice, making the listening experience much more engaging.


### 🗣️ Included TTS Models
All Coqui TTS models-(Tacotron, Tacotron2, Glow-TTS, Speedy-Speech, Align-TTS, FastPitch, FastSpeech, FastSpeech2, SC-GlowTTS, Capacitron, OverFlow, Neural HMM TTS, Delightful TTS, ⓍTTS, VITS, 🐸 YourTTS, 🐢 Tortoise, 🐶 Bark), and STYLETTS2.


<details>
<summary> 🌍🎙️ Accents you can give each character with the default cloning model (XTTS) </summary>
  - They also allow them to speak these languages, but the quotation attribution won't correctly identify for anything thats not English.
English (en),
Spanish (es),
French (fr),
German (de),
Italian (it),
Portuguese (pt),
Polish (pl),
Turkish (tr),
Russian (ru),
Dutch (nl),
Czech (cs),
Arabic (ar),
Chinese (zh-cn),
Japanese (ja),
Hungarian (hu),
Korean (ko)
</details>

### outputs as a m4b with all book metadata and chapters, example output file in a audiobook player app
![Example_of_output_in_audiobook_program](https://github.com/DrewThomasson/VoxNovel/blob/dc5197dff97252fa44c391dc0596902d71278a88/readme_files/example_in_app.jpeg)

(as well as a folder of individual mp4 chatper files with ebook image embedded in them if you want that)

## 🔊 DEMOS
 **High Quality XTTS V2 Demos**
 
https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/9e10b36d-b2e9-4462-8bad-13a3d8fce192
<details>
  
<summary> 🔊🎉 More Demo Audio files :) </summary>


 **High Quality Tortoise Demos**
 
https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/94e23918-b7e1-4399-935e-179dd12212c3

 **Super fast audio Balacoon Demos**
 
https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/5e3c5501-4c87-462b-a11b-a15f546e51f4


https://github.com/DrewThomasson/VoxNovel-OLD-/assets/126999465/f4e57afe-53df-485c-81ff-65d7dcf29cb5

 **Super High Quality testing with fine tuned models **

https://github.com/DrewThomasson/bark/assets/126999465/5da79b9d-2974-471e-a564-31a180ba2833
</details>

You can fine tune your own Xtts models with around 6+ minutes of audio for free with this colab
https://colab.research.google.com/drive/1GiI4_X724M8q2W-zZ-jXo7cWTV7RfaH-

## GUI

<img width="200" alt="gui_1_select_file" src="https://github.com/DrewThomasson/VoxNovel/blob/e39b5e742c57cc3f88aa7549a5ce5517f392103e/readme_files/gui_1_select_file.png">
<details>
<summary> GUI Part 1 (BookNLP Processor) Info/Features </summary>
  -"Process File" button: Click and it'll ask you to select a ebook file.
</details>
<img width="1000" alt="gui_2_finetune" src="https://github.com/DrewThomasson/VoxNovel/blob/e39b5e742c57cc3f88aa7549a5ce5517f392103e/readme_files/gui_3_finetune.png">
<details>
<summary> GUI Part 2 (Coqui TTS GUI) Info/Features </summary>

- **Select TTS Model Dropdown:** This selects the TTS model that will be used for voice cloning.
- **Include fast Voice Models Checkbox:** (Fast generate at cost of audio quality) Click this to be able to see every other model and singular voices supported by Coqui TTS.
  - It will update the "Select TTS Model" Dropdown for voice cloning models to also include (List of values to be added).
  - It will update the Dropdown for voices to select for each character to also include (List of values to be added).
- **Make all audio generate with Narrator voice Checkbox:** This will make every character's audio be generated with the voice you have selected for the Narrator when you click the "Generate audio" button.
- **Clone new voice Button:** Click this to add a new voice you can clone (make sure you have a reference audio file on hand).
- **Add Fine-tuned Xtts model to voice actor Button:** If you have a folder containing all the parameters of a fine-tuned Xtts model of a specific voice, then you can click this to make that voice actor clone with that fine-tuned Xtts model, to provide much better voice cloning results.
- **Character voices Dropdowns:** These are the dropdowns for selecting the Voice Actor (and the Accent of each character if using XTTS).
  - (1): The Voice actors available to select from for this character. (Default value is audio selected based on inferred gender of character being: "F, M, Other").
     - When you select a voice It will play the audio sample of that voice, if it's a fast voice model voice and a refrence audio does not exist, then it will generate one to play.
  - (2): The Accents available to select from for this character. (Optional, Default is English).
- **Chapter Delimiter Field:** Will change the default chapter delimiter (The string that's used to identify chapters).
- **Silence Duration in milliseconds (ms) Field:** This will change the amount of milliseconds in between each combined chunk of audio.
- **Select TTS Language Dropdown:** This will let you select the default Accent used for every character which has not had the Accent manually selected for.
- **Loading bar:** Will give an approximate amount of time left. (Estimate, you probably won't see accurate predictions until it's been running for 5 min).
- **Annotated book preview Block:** This will show the entirety of the book with each character's lines color-coded.
  - You can click on a line while the audiobook is being generated to hear what that generated line sounds like. But only if the line has already had audio generated for it; if not, it'll play nothing.
- **Load Book Button:** Clicking this will reload the color-coded annotated book view, it will just randomize the selected colors for each character's lines.
- **Generate Audio Button:** Will start generating the full audiobook.
- **Select random voices Button (Will only be visible if the "include fast Voice Models" checkbox is checked):** Will Select an auto-gender-inferred fast model voice for every character except for the narrator's voice.

</details>
<img width="585" alt="gui_3_run" src="https://github.com/DrewThomasson/VoxNovel/blob/e39b5e742c57cc3f88aa7549a5ce5517f392103e/readme_files/gui_2_run.png">
<details>
<summary> GUI Part 3 (Book Viewer) Info/Features </summary>
  -It's hard to explain its more of a playground if you mess around with it then you should get how it works. But it can be used to fine tune the audiobook
  -Close out of the window when your done with it.
</details>

## 📦 SetUp Install

Run in this order:


<details>
<summary> 🐧 Linux </summary>
##  Single command Ubuntu install:(Do not use if you already have miniconda installed.)
1. `yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu-install.sh | bash`
-This will also create a desktop shortcut to run Voxnovel as well.


##  or manual install:
1. `sudo apt-get install calibre`
2. `sudo apt-get install ffmpeg`
3. `conda create --name VoxNovel python=3.10`
4. `conda activate VoxNovel`
5. `git clone https://github.com/DrewThomasson/VoxNovel.git`
6. `cd VoxNovel`
7. `pip install bs4`
8. `pip install styletts2`
9. `pip install tts==0.21.3`
10. `pip install booknlp`
11. `pip install -r Ubuntu_requirements.txt`
12. `python -m spacy download en_core_web_sm`
</details>

<details>
<summary> Steam Deck) (x86_64 Arch Linux) </summary>

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
15. `pip install styletts2`
16. `pip install tts==0.21.3`
17. `pip install booknlp`
18. `pip install -r SteamDeck_requirements.txt`
19. `pip3 install spacy`
20. `python3 -m spacy download en_core_web_sm`
21. `sudo pacman -S calibre`
22. mv ~/miniconda3/envs/VoxNovel/lib/libstdc++.so.6 ~/miniconda3/envs/tts/lib/libstdc++.so.6.bak

23. `pip install mechanize`
24. `pip install bs4`
25. `pip install css_parser`
</details>


<details>
<summary> Intel mac </summary>

1. `brew install calibre`
2. `brew install ffmpeg`
3. `conda create --name VoxNovel python=3.10`
4. `conda activate VoxNovel`
5. `git clone https://github.com/DrewThomasson/VoxNovel.git`
6. `cd VoxNovel`
7. `pip install styletts2`
8. `pip install tts==0.21.3`
9. `pip install booknlp`
9.`pip install -r MAC-requirements.txt`
10. `pip install spacy`
11.`python -m spacy download en_core_web_sm`
</details>


<details>
<summary> Windows 11 </summary>
Because of BookNLP Windows issues, all of this will be run in WSL (don't worry, it's still easy).

1. In your PowerShell, paste `wsl --install` to install WSL.
2. In your PowerShell, paste `wsl --update --pre-release` to update WSL to a pre-release version, right now the prerelease has all the sound and such working.

3. After you set the username and password, you'll now be able to open WSL as an application. This will allow you to run Ubuntu software. You'll now want to open WSL if you closed it and paste these commands.

   (This will install Calibre for ebook conversion)
   `cd ~`
   `sudo apt update`
   `sudo apt upgrade`
   `sudo apt install calibre`
    `sudo apt install ffmpeg`

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
   `pip isntall styletts2`
   `pip install tts==0.21.3`
   `pip install booknlp`
   `pip install -r Ubuntu_requirements.txt`
   `pip install spacy`
   `python -m spacy download en_core_web_sm`
   `sudo apt install espeak-ng`

You can access the files on your WSL Ubuntu in Windows File Explorer by putting this into the address: `\\wsl.localhost\Ubuntu\home\`
</details>


## 🚀 To Run the program
`python gui_run.py`
<details>
<summary> Running with Low VRAM (4 GB) </summary>

### Modifications
- Turns out once you set the device it stays like that for the full program.
- So, I've split the program into two Python programs: one CPU and one GPU. I've tested this on my (4GB VRAM GPU) and this solution works. at least on my end I really hope it works on your end. 🙏


### To run the fix I've made tailor made for a low Vram GPU situation:

To run the provided scripts on your system, follow these steps in order:

1. **Book Processing (CPU Only):** 
   - Script: [1CPU_Book_processing.py](https://github.com/DrewThomasson/VoxNovel/blob/main/1CPU_Book_processing.py)
   - This script handles the task of only processing the book using BookNLP, specifically forcing it to run on the CPU.
   - Run with 'python 1CPU_Book_processing.py'

2. **Audio Generation (GPU Only):**
   - Script: [2GPU_Audio_generation.py](https://github.com/DrewThomasson/VoxNovel/blob/main/2GPU_Audio_generation.py)
   - This script is dedicated to only generating audio with the GPU and should be run after completing the book processing with `1CPU_Book_processing.py`.
   - Run with 'python 2GPU_Audio_generation.py'

### Performance Results

Upon running a mini test with an epub file using the above setup, the following performance metrics were observed:

### Performance Results
Testing on done with the mini epub file located in the Example_working_files.zip

| Task               | Configuration                                                    | Time (Seconds)       |
|--------------------|------------------------------------------------------------------|----------------------|
| **Book Processing**    | GPU only (GeForce GTX 980), 4GB VRAM, 32GB RAM, Intel i7-8700K   | 2.922                |
| **Audio Generation**   | GPU only (GeForce GTX 980), 4GB VRAM, 32GB RAM, Intel i7-8700K   | 128.48               |
| **Book Processing**    | CPU only, 32GB RAM, Intel i7-8700K                              | 4.964                |
| **Audio Generation**   | CPU only, 32GB RAM, Intel i7-8700K                              | 391.4227    |

</details>

<details>
<summary> To Run the auto program (Don't use temporarily on hold) </summary>
This means all you do is select the book and all the voices will be auto assigned and generated for you.

`python auto_noGui_run.py`
</details>


## 📚 Supported ebook File Types: 
.epub, .pdf, .mobi, .txt, .html, .rtf, .chm, .lit, .pdb, .fb2, .odt, .cbr, .cbz, .prc, .lrf, .pml, .snb, .cbc, .rb, and .tcr,

 - (Best results are from using epub or mobi for auto chapter detection)


## Folders
<details>
  
<summary> 📂 Folders used by the program </summary>
/Final_combined_output_audio: This is where all of your chapter audio files will be put in order of chapter num

/output_audiobooks: This is where all of your m4b audiobook files will be stored

/Working_files: Holds all of the working files used by the program while activly running.

/tortoise: Holds all the sample voice files
</details>

## GUI functions
<details>
<summary> GUI Part 1 (BookNLP Processor) </summary>
  -"Process File" button: Click and it'll ask you to select a ebook file.
</details>

<details>
<summary> GUI Part 2 (Coqui TTS GUI) </summary>

- **Select TTS Model Dropdown:** This selects the TTS model that will be used for voice cloning.
- **Include fast Voice Models Checkbox:** (Fast generate at cost of audio quality) Click this to be able to see every other model and singular voices supported by Coqui TTS.
  - It will update the "Select TTS Model" Dropdown for voice cloning models to also include (List of values to be added).
  - It will update the Dropdown for voices to select for each character to also include (List of values to be added).
- **Make all audio generate with Narrator voice Checkbox:** This will make every character's audio be generated with the voice you have selected for the Narrator when you click the "Generate audio" button.
- **Clone new voice Button:** Click this to add a new voice you can clone (make sure you have a reference audio file on hand).
- **Add Fine-tuned Xtts model to voice actor Button:** If you have a folder containing all the parameters of a fine-tuned Xtts model of a specific voice, then you can click this to make that voice actor clone with that fine-tuned Xtts model, to provide much better voice cloning results.
- **Character voices Dropdowns:** These are the dropdowns for selecting the Voice Actor (and the Accent of each character if using XTTS).
  - (1): The Voice actors available to select from for this character. (Default value is audio selected based on inferred gender of character being: "F, M, Other").
     - When you select a voice It will play the audio sample of that voice, if it's a fast voice model voice and a refrence audio does not exist, then it will generate one to play.
  - (2): The Accents available to select from for this character. (Optional, Default is English).
- **Chapter Delimiter Field:** Will change the default chapter delimiter (The string that's used to identify chapters).
- **Silence Duration in milliseconds (ms) Field:** This will change the amount of milliseconds in between each combined chunk of audio.
- **Select TTS Language Dropdown:** This will let you select the default Accent used for every character which has not had the Accent manually selected for.
- **Loading bar:** Will give an approximate amount of time left. (Estimate, you probably won't see accurate predictions until it's been running for 5 min).
- **Annotated book preview Block:** This will show the entirety of the book with each character's lines color-coded.
  - You can click on a line while the audiobook is being generated to hear what that generated line sounds like. But only if the line has already had audio generated for it; if not, it'll play nothing.
- **Load Book Button:** Clicking this will reload the color-coded annotated book view, it will just randomize the selected colors for each character's lines.
- **Generate Audio Button:** Will start generating the full audiobook.
- **Select random voices Button (Will only be visible if the "include fast Voice Models" checkbox is checked):** Will Select an auto-gender-inferred fast model voice for every character except for the narrator's voice.

</details>


<details>
<summary> GUI Part 3 (Book Viewer) </summary>
  -It's hard to explain its more of a playground if you mess around with it then you should get how it works. But it can be used to fine tune the audiobook
  -Close out of the window when your done with it.
</details>

## 🌟 Features

- [x] Free and entirely locally run
- [x] Supports all ebook file formats by using calibre
- [x] Can run on CPU or CUDA GPU
- [x] Autoselects a starting estimated voice by pronouns per character
- [x] Supports all models in Coqui TTS and all voices in the models
- [x] Easily create a new voice actor in seconds through voice cloning in GUI
- [x] Can play audio by clicking on the text in the book viewer in GUI
- [x] Ability to regenerate specific lines if they came out weird
- [x] Ability to add custome fine tuned models for specific voice with the click of a button in GUI
- [x] Outputs a single file output as m4b to include all the metadata(chapters book image ect)
- [x] Supports STYLETTS2 as a model you can select from for voice cloning for WICKED FAST speed (even on cpu)
- [x] Includes 26 default voices for cloning


## 🔜 Incoming Planned Features
- [ ] Ability to change the character for a line if incorrectly attributed by booknlp
- [ ] Make it so that all the included voices and models already have their premade own demo voices
- [ ] Make it so that the demo audio for the cloned voices is not their reference audio but what their voices sound like generated
- [ ] Using whisper transcriptions to cut hallucinations out of generated audio
- [ ] Adding a low vram checkbox option in gui
- [ ] Incorporating local model to generate sound effects when a book discribes a location or sound effect

## 🙏 Special thanks to:
-@sidharthrajaram
(for his Styletts2 pip install he created, I couldn't of added styletts2 without him. :)  )
(https://github.com/sidharthrajaram/StyleTTS2)
