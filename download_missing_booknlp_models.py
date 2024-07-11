import os
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

# Define the URL and file name
url = "https://huggingface.co/drewThomasson/Booknlp_models_Backup/resolve/main/booknlp_models.zip?download=true"
file_name = "booknlp_models.zip"

# Get the user's home directory
home_dir = str(Path.home())

# Full path for the zip file
zip_path = os.path.join(home_dir, file_name)

# Download the file with a progress bar
print("Downloading the missing booknlp model files...")
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

# Unzip the file
print("Unzipping the unzipping the booknlp files...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(home_dir)

# Delete the zip file
print("Deleting the zip file...")
os.remove(zip_path)

print("Process completed successfully!")
