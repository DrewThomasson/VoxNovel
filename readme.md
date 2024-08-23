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

You can fine-tune your own Xtts models with around 6+ minutes of audio for free with this colab ~~[https://colab.research.google.com/drive/1GiI4_X724M8q2W-zZ-jXo7cWTV7RfaH-](https://colab.research.google.com/drive/1GiI4_X724M8q2W-zZ-jXo7cWTV7RfaH-)~~

Edit: that colab doesn't work anymore: use my version that provides a fix: [https://colab.research.google.com/drive/1sqQqzupo2pdjgggkrbM60sU6sBFYo3su?usp=sharing](https://colab.research.google.com/drive/1sqQqzupo2pdjgggkrbM60sU6sBFYo3su?usp=sharing)


## 🤖 Headless VoxNovel Google Colab

Explore and run the interactive version of the Headless VoxNovel project directly on Google Colab! Get started [here](https://colab.research.google.com/drive/15pp2hFBo2fD3legDQfWY5DMt-aI-HKKF?usp=sharing).

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

<details>
<summary> 🤖 Headless VoxNovel Google Colab</summary>

Explore and run the interactive version of the Headless VoxNovel project directly on Google Colab! Get started [here](https://colab.research.google.com/drive/15pp2hFBo2fD3legDQfWY5DMt-aI-HKKF?usp=sharing).

</details>
<details>
<summary> 🐳 Docker (Sound not working in gui yet) </summary>
<details>
<summary>🐳 Headless Docker</summary>
<details>
<summary>Docker headless m1 🍏Mac</summary>

1. `cd ~`
  
2. `git clone https://github.com/DrewThomasson/VoxNovel.git`
3. `sudo docker run -v "$HOME/VoxNovel:/VoxNovel/" -it athomasson2/voxnovel:headless_m1_v2`

</details>
<details>
<summary>Headless Docker 🐧 Linux/Intel 🍏Mac</summary>

## For Headless Docker on only cpu

1. `cd ~`
  
2. `git clone https://github.com/DrewThomasson/VoxNovel.git`
3. `sudo docker run -v "$HOME/VoxNovel:/VoxNovel/" -it athomasson2/voxnovel:latest_headless`

## For headless docker with gpu speedup if you have a nvida gpu

1. `cd ~`
  
2. `git clone https://github.com/DrewThomasson/VoxNovel.git`
3. `sudo docker run --gpus all -v "$HOME/VoxNovel:/VoxNovel/" -it athomasson2/voxnovel:latest_headless`

</details>
<details>
<summary>Headless Docker 🖥️ Windows</summary>

### Installation and Setup on Windows (PowerShell)

Follow these steps to set up the VoxNovel project on a Windows system using PowerShell:

1. Navigate to your user profile directory:
   ```powershell
   cd $env:USERPROFILE
   ```

2. Clone the VoxNovel repository from GitHub:
   ```powershell
   git clone https://github.com/DrewThomasson/VoxNovel.git
   ```

### Running VoxNovel in Docker

#### For Headless Operation on CPU

To run the VoxNovel application in a Docker container on your CPU:

```powershell
docker run -v "${env:USERPROFILE}/VoxNovel/:/VoxNovel/" -it athomasson2/voxnovel:latest_headless
```

#### For Headless Operation with NVIDIA GPU Speedup

If you have an NVIDIA GPU and want to accelerate processing, use the following command:

```powershell
docker run --gpus all -v "${env:USERPROFILE}/VoxNovel/:/VoxNovel/" -it athomasson2/voxnovel:latest_headless
```
</details>
</details>
<details>
<summary> 🐳 GUI Docker (Sound not working in gui yet) </summary>
<details>
<summary> 🐧  Linux Docker </summary>
1. `cd ~`
  
2. `git clone https://github.com/DrewThomasson/VoxNovel.git`
3. `sudo docker run --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/snd:/dev/snd --device /dev/snd -v "$HOME/VoxNovel:/VoxNovel/" -it athomasson2/voxnovel:latest`
</details>


<details>
<summary> 🍏 Mac Docker </summary>

## Setting Up GUI Applications with Docker on macOS

This guide provides instructions on how to run a Docker container with a graphical user interface on macOS using XQuartz for X11 forwarding and volume mounting.

### Install XQuartz

1. Download and install XQuartz from [XQuartz website](https://www.xquartz.org/).
2. Open XQuartz.
3. Go to `XQuartz` -> `Preferences`.
4. In the `Security` tab, enable **Allow connections from network clients**.
5. Restart XQuartz to apply these settings.

### Configure and Run the Docker Container

#### Allow Docker to Connect to XQuartz

Open a terminal and run the following command to allow connections from your local machine to XQuartz:

    xhost + $(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')

#### Start the Docker Container

Run the following command to start your Docker container. This command configures the GUI to display on your host and mounts the necessary directories:
```
cd ~
git clone https://github.com/DrewThomasson/VoxNovel.git
docker run -e DISPLAY=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'):0 \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -v "/Users/$(whoami)/VoxNovel:/VoxNovel" \
           athomasson2/voxnovel:latest
```

### Notes

- **XQuartz Configuration**: Ensure that XQuartz is configured to allow network clients before attempting to connect.
- **Directory Existence**: Verify that the directory `/Users/$(whoami)/VoxNovel` exists on your Mac. If not, create it or adjust the volume mount path in the Docker command as needed.
- **Firewall and Security**: If you face connectivity issues, check any firewall settings and security preferences that might block the connections.

</details>

<details>
  <summary>🪟 Windows Docker</summary>
  
  1. Install VcXsrv:
     ```sh
     choco install vcxsrv
     ```
     - First install VcXsrv and configure it to allow connections.
     
     <details>
       <summary>How to setup VcXsrv</summary>
       
       After installing VcXsrv, it typically launches automatically. You can confirm it's running by checking for its icon in the system tray, usually located near the clock in the taskbar. It may also start automatically when you log in to your system.
       
       To ensure it's configured to allow connections from Docker containers, follow these steps:
       
       1. Right-click on the VcXsrv icon in the system tray.
       2. Select "XLaunch" to open the configuration wizard.
       3. In the configuration wizard, select "Multiple windows" and proceed to the next step.
       4. Choose your preferred settings for display number and screen.
       5. In the "Extra settings" window, make sure to check the box labeled "Disable access control" to allow connections from Docker containers.
       6. Complete the configuration by clicking "Finish" and then "Save configuration" when prompted.
       
       With these settings, VcXsrv should be running and configured to allow connections from Docker containers. You can now proceed with running your Docker commands requiring GUI support.
     </details>
     
  2. Change to your home directory:
     ```sh
     cd $HOME
     ```
  3. Clone the repository:
     ```sh
     git clone https://github.com/DrewThomasson/VoxNovel.git
     ```
  4. Run the Docker container:
     ```sh
     docker run -e DISPLAY=host.docker.internal:0 -v "/Users/$(whoami)/VoxNovel:/VoxNovel/" -it athomasson2/voxnovel:latest
     ```
</details>

</details>
</details>
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
10. `pip install booknlp==1.0.7.1`
11. `pip install -r Ubuntu_requirements.txt`
12. `python -m spacy download en_core_web_sm`



<details>
<summary> 🈳 For non Latin-based Languages TTS support (Optional)</summary>

Install Mecab for (Non Latin-based Languages tts support)(Optional):
- Ubuntu: `sudo apt-get install -y mecab libmecab-dev mecab-ipadic-utf8`

(For non Latin-based Languages tts support)(Optional)  
`python -m unidic download`
```bash
pip install mecab mecab-python3 unidic
```
</details>
</details>

<details>
<summary> 🔲 Steam Deck) (x86_64 Arch Linux) </summary>

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
17. `pip install booknlp==1.0.7.1`
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
<summary> 🍏 Intel mac </summary>
Run in this order:

1. `brew install calibre`
2. `brew install ffmpeg`
3. `conda create --name VoxNovel python=3.10`
4. `conda activate VoxNovel`
5. `git clone https://github.com/DrewThomasson/VoxNovel.git`
6. `cd VoxNovel`
7. `pip install styletts2`
8. `pip install tts==0.21.3`
9. `pip install booknlp==1.0.7.1`
9.`pip install -r MAC-requirements.txt`
10. `pip install spacy`
11.`python -m spacy download en_core_web_sm`


<details>
<summary> 🈳 For non Latin-based Languages TTS support (Optional)</summary>

Install Mecab for (Non Latin-based Languages tts support)(Optional):
- macOS: `brew install mecab`, `brew install mecab-ipadic`

(For non Latin-based Languages tts support)(Optional)  
`python -m unidic download`
```bash
pip install mecab mecab-python3 unidic
```
</details>
</details>

<details>
<summary> 🍏 Apple Silicon Mac (Tested on 2020 M1 pro 8gb ram)</summary>
Run in this order:

1. `brew install calibre`(You might have to also install it manually from their site if this doesn't work)
2. `brew install ffmpeg`
3. `conda create --name VoxNovel python=3.10`
4. `conda activate VoxNovel`
5. `git clone https://github.com/DrewThomasson/VoxNovel.git`
6. `cd VoxNovel`
7. `pip install tensorflow-macos` (Also optional `pip install tensorflow-metal` But so far I haven't gotten gpu speedup yet
8. `pip install styletts2`
9. `pip install tts==0.21.3`
10. `pip install --no-dependencies booknlp==1.0.7.1`
11. `pip install transformers==4.30.0`
12. `pip install tensorflow`
13. `pip install -r MAC-requirements.txt`
14. `pip install ebooklib bs4 epub2txt pygame moviepy spacy`
15. `python -m spacy download en_core_web_sm`



<details>
<summary> 🈳 For non Latin-based Languages TTS support (Optional)</summary>

Install Mecab for (Non Latin-based Languages tts support)(Optional):
- macOS: `brew install mecab`, `brew install mecab-ipadic`
(For non Latin-based Languages tts support)(Optional)  
`python -m unidic download`
```bash
pip install mecab mecab-python3 unidic
```
</details>

</details>
<details>
<summary> 🪟 Windows 11 </summary>
  
### Because of BookNLP Windows issues, all of this will be run in WSL (don't worry, it's still easy).
  
## 🎥 Watch the installation video [here](https://youtu.be/OmJub3uvfz4)

1. In your PowerShell, paste:
   ```sh
   wsl --install
   ```
   to install WSL. (You might be prompted by your system to enable virtualization in your BIOS if it's available, as it is needed to run WSL on Windows.)

2. After setting your username and password, open WSL and paste this command for a single command install:
   ```sh
   yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu-install.sh | bash
   ```

3. **(Optional only for Nvida graphics cards Do not run this command if you don't have a Nvidia graphics card)** Install the NVIDIA CUDA toolkit (required for Nvidia GPU acceleration):
   ```sh
   sudo apt install nvidia-cuda-toolkit
   ```

4. Make sure you are in the VoxNovel conda environment:(If 'conda: command not found
' IE- conda is not seen as a command then try closing out of the current powershell window and relaunching the wsl env with   [ wsl -d Ubuntu   ]
     ```sh
   conda activate VoxNovel
   ```

5. Navigate to the VoxNovel folder (if not already there):
   ```sh
   cd ~ && cd VoxNovel
   ```

6. Now just run one of the two programs shown below ⬇️

## 🚀 To Run the program
   ```sh
   python gui_run.py
   ```

## 🚀 Or to run headless
   ```sh
   python headless_voxnovel.py
   ```

## 🌐 Access WSL Ubuntu Files from Windows

You can access your WSL Ubuntu files directly in Windows File Explorer by entering the following path in the address bar:

```
\\wsl.localhost\Ubuntu\home\
```
The output audiobook files will be located under `VoxNovel\output_audiobooks` in the wsl env

## 🎯 To Create VoxNovel Windows Desktop Shortcut

Run this command in powershell

```bash
Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/create_desktop_shortcut.ps1").Content
```


### 🗑️ Uninstallation:

To remove everything, run the following command in PowerShell:

```sh
wsl --unregister Ubuntu
```

This will completely remove the Ubuntu environment where the application is stored. 🚮

### 🛠️ Troubleshooting WSL

If you have trouble with the WSL environment:

1. List all WSL environments:
   ```sh
   wsl --list --verbose
   ```

2. Remove a specific WSL environment (e.g., Ubuntu):
   ```sh
   wsl --unregister <distro_name>
   ```

3. Reinstall WSL:
   ```sh
   wsl --install
   ```

To launch WSL anytime you need to run this program, you can use the search bar in Windows to find and launch "WSL" or run:
   ```sh
   wsl
   ```

</details>


<details>
<summary> 🈳 For non Latin-based Languages TTS support (Optional)</summary>

Install Mecab for (Non Latin-based Languages tts support)(Optional):
- `sudo apt-get install -y mecab libmecab-dev mecab-ipadic-utf8`

(For non Latin-based Languages tts support)(Optional)  
`python -m unidic download`
```bash
pip install mecab mecab-python3 unidic
```
</details>
</details>


## 🚀 To Run the program
   ```sh
   python gui_run.py
   ```

## 🚀 Or to run headless
   ```sh
   python headless_voxnovel.py
   ```

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
   - Run with `python 1CPU_Book_processing.py`

2. **Audio Generation (GPU Only):**
   - Script: [2GPU_Audio_generation.py](https://github.com/DrewThomasson/VoxNovel/blob/main/2GPU_Audio_generation.py)
   - This script is dedicated to only generating audio with the GPU and should be run after completing the book processing with `1CPU_Book_processing.py`.
   - Run with `python 2GPU_Audio_generation.py`

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
<summary> To Run the auto program </summary>
This means all you do is select the book and all the voices will be auto assigned and generated for you.

`python auto_noGui_run.py`
</details>

## 🌐 Access generated audiobook files

You can access your generated audiobook files in the VoxNovel folder at the location

```
VoxNovel/output_audiobooks
```

## 📚 Supported ebook File Types: 
.epub, .pdf, .mobi, .txt, .html, .rtf, .chm, .lit, .pdb, .fb2, .odt, .cbr, .cbz, .prc, .lrf, .pml, .snb, .cbc, .rb, and .tcr,

 - (Best results are from using epub or mobi for auto chapter detection)


## Folders
<details>
  
<summary> 📂 Folders used by the program </summary>

/Final_combined_output_audio: This is where all of your chapter audio files will be put in order of chapter num



/output_audiobooks: This is where all of your m4b audiobook files will be stored


/Working_files: Holds all of the working files used by the program while activly running.
 - /Working_files/temp_ebook: Holds all of the individual extracted chapter txt files from the ebook.

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
- [x] Low vram option(Details in readme)
- [x] Gui Docker image (Graphical interface-no sound in gui yet)
- [x] Headless version of docker image
- [x] Headless version of VoxNovel
- [x] A Google Colab using the headless version
- [x] Desktop Shortcut for Ubuntu Linux 🐧
- [x] Desktop Shortcut for Windows 11 🪟

## 🔜 Incoming Planned Features
- [ ] Ability to change the character for a line if incorrectly attributed by booknlp
- [ ] Make it so that all the included voices and models already have their premade own demo voices
- [ ] Make it so that the demo audio for the cloned voices is not their reference audio but what their voices sound like generated
- [ ] Using whisper transcriptions to cut hallucinations out of generated audio
- [ ] Incorporating local model to generate sound effects when a book discribes a location or sound effect
- [ ] Adding Save file functionaly

## 🙏 Special thanks to:
-@sidharthrajaram
(for his Styletts2 pip install he created, I couldn't of added styletts2 without him. :)  )
(https://github.com/sidharthrajaram/StyleTTS2)
