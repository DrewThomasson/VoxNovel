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
