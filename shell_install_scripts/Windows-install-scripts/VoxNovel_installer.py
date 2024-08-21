import os
import subprocess
import requests
import tempfile

# URLs of the PowerShell scripts
scripts = [
    "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/install_wsl.ps1",
    "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/run_ubuntu_autoinstaller_in_wsl.ps1",
    "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/create_desktop_shortcut.ps1"
]

def download_script(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    script_path = os.path.join(tempfile.gettempdir(), os.path.basename(url))
    with open(script_path, 'w') as file:
        file.write(response.text)
    return script_path

def run_script(script_path):
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)

def main():
    for url in scripts:
        print(f"Downloading {url}...")
        script_path = download_script(url)
        print(f"Running {script_path}...")
        run_script(script_path)
        input("Press Enter to proceed to the next step...")

if __name__ == "__main__":
    main()
