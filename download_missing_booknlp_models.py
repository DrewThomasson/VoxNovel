import os
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

def download_and_extract():
    url = "https://huggingface.co/drewThomasson/Booknlp_models_Backup/resolve/main/booknlp_models.zip?download=true"
    file_name = "booknlp_models.zip"
    home_dir = str(Path.home())
    zip_path = os.path.join(home_dir, file_name)
    models_folder = os.path.join(home_dir, "booknlp_models")

    print("Downloading the missing booknlp files...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(zip_path, 'wb') as file, tqdm(
        desc=file_name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

    print("Extracting required files...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith('booknlp_models/') and file.split('/')[-1] in required_files:
                zip_ref.extract(file, home_dir)

    print("Deleting the zip file...")
    os.remove(zip_path)

    print("Process completed successfully!")

# List of required files
required_files = [
    "coref_google_bert_uncased_L-12_H-768_A-12-v1.0.model",
    "speaker_google_bert_uncased_L-12_H-768_A-12-v1.0.1.model",
    "entities_google_bert_uncased_L-6_H-768_A-12-v1.0.model"
]

# Get the user's home directory
home_dir = str(Path.home())
models_folder = os.path.join(home_dir, "booknlp_models")

# Check if the folder exists, if not create it
if not os.path.exists(models_folder):
    os.makedirs(models_folder)

# Check for missing files
missing_files = [file for file in required_files if not os.path.exists(os.path.join(models_folder, file))]

if missing_files:
    print(f"The following files are missing: {', '.join(missing_files)}")
    print("Downloading and extracting required files...")
    download_and_extract()
else:
    print("All required booknlp files are present. No action needed.")
