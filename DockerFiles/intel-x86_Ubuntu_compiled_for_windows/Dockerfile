# Use an official Python 3.10 image
FROM python:3.10-slim-buster

# Set non-interactive installation to avoid timezone and other prompts
ENV DEBIAN_FRONTEND=noninteractive





# Copy the requirements file to the correct directory
COPY Windows-requirements.txt /VoxNovel/

# Update the package list and install necessary packages
RUN apt-get update && apt-get install -y \
    libxcb-cursor0 \
    wget && \
    # Install Calibre
    wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin

# Add Calibre to PATH
ENV PATH="/opt/calibre:$PATH"

# Create and run the ebook conversion test script
RUN echo "import subprocess" > /tmp/calibre_test.py && \
    echo "def convert_to_epub(input_path, output_path):" >> /tmp/calibre_test.py && \
    echo "    try:" >> /tmp/calibre_test.py && \
    echo "        subprocess.run(['ebook-convert', input_path, output_path], check=True)" >> /tmp/calibre_test.py && \
    echo "    except subprocess.CalledProcessError as e:" >> /tmp/calibre_test.py && \
    echo "        print(f'An error occurred while converting the eBook: {e}')" >> /tmp/calibre_test.py && \
    echo "        return False" >> /tmp/calibre_test.py && \
    echo "    except Exception as e:" >> /tmp/calibre_test.py && \
    echo "        print(f'An unexpected error occurred: {e}')" >> /tmp/calibre_test.py && \
    echo "        return False" >> /tmp/calibre_test.py && \
    echo "    return True" >> /tmp/calibre_test.py && \
    echo "input_path = '/VoxNovel/Windows-requirements.txt'" >> /tmp/calibre_test.py && \
    echo "output_path = '/VoxNovel/Windows-requirements.epub'" >> /tmp/calibre_test.py && \
    python3 /tmp/calibre_test.py && \
    rm '/VoxNovel/Windows-requirements.epub'


# Removing unused files to clean up space
RUN apt-get clean && rm -rf /var/lib/apt/lists/*






# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    espeak \
    espeak-ng \
    ffmpeg \
    wget \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /VoxNovel

# Clone the VoxNovel repository and install dependencies
RUN git clone https://github.com/DrewThomasson/VoxNovel.git .

# Installing dependencies separately to handle potential conflicts
RUN pip install --upgrade pip
RUN pip install bs4
RUN pip install styletts2
RUN pip install tts==0.21.3
RUN pip install booknlp
RUN pip install -r Ubuntu_requirements.txt
RUN pip install spacy && python -m spacy download en_core_web_sm

#To get the optional setup of the non-latin languages to work in this VoxNovel image
RUN apt-get update && \
    apt-get install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    build-essential

RUN pip install unidic

RUN python -m unidic download

RUN pip install mecab-python3



COPY 1.wav /VoxNovel/


# Run of XTTS to get it set up in the docker image
RUN echo "import torch" > /tmp/script1.py && \
    echo "from TTS.api import TTS" >> /tmp/script1.py && \
    echo "device = 'cuda' if torch.cuda.is_available() else 'cpu'" >> /tmp/script1.py && \
    echo "print(TTS().list_models())" >> /tmp/script1.py && \
    echo "tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to(device)" >> /tmp/script1.py && \
    echo "wav = tts.tts(text='Hello world!', speaker_wav='1.wav', language='en')" >> /tmp/script1.py && \
    echo "tts.tts_to_file(text='Hello world!', speaker_wav='1.wav', language='en', file_path='output.wav')" >> /tmp/script1.py && \
    yes | python3 /tmp/script1.py


# Remove that test audio file
RUN rm output.wav



#COPY Windows-requirements.txt /VoxNovel/




#Run of bookNLP get it set up in the docker image
RUN echo 'from booknlp.booknlp import BookNLP' > /tmp/script2.py && \
    echo 'model_params = {' >> /tmp/script2.py && \
    echo '    "pipeline": "entity,quote,supersense,event,coref",' >> /tmp/script2.py && \
    echo '    "model": "big"' >> /tmp/script2.py && \
    echo '}' >> /tmp/script2.py && \
    echo 'booknlp = BookNLP("en", model_params)' >> /tmp/script2.py && \
    echo 'input_file = "Windows-requirements.txt"' >> /tmp/script2.py && \
    echo 'output_directory = "output_dir/bartleby/"' >> /tmp/script2.py && \
    echo 'book_id = "bartleby"' >> /tmp/script2.py && \
    echo 'booknlp.process(input_file, output_directory, book_id)' >> /tmp/script2.py && \
    python3 /tmp/script2.py

# Remove the test BookNLP files
RUN rm -rf /output_dir







# Set the command to run your GUI application
#CMD ["python", "gui_run.py"]
CMD ["python", "headless_voxnovel.py"]
