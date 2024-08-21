import os
import subprocess
import requests
import tempfile
import tkinter as tk
from tkinter import messagebox

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

def on_next():
    global script_index
    if script_index < len(scripts):
        script_url = scripts[script_index]
        script_path = download_script(script_url)
        run_script(script_path)
        script_index += 1
        if script_index < len(scripts):
            next_button.config(text=f"Run Step {script_index + 1}")
        else:
            next_button.config(text="Finish", state="disabled")
            messagebox.showinfo("Completed", "All steps completed!")
    else:
        root.quit()

# Set up the main application window
root = tk.Tk()
root.title("VoxNovel Installer")

script_index = 0

# Create a label and a button in the window
label = tk.Label(root, text="Press 'Next' to run each step of the installation.", padx=20, pady=20)
label.pack()

next_button = tk.Button(root, text="Run Step 1", command=on_next, padx=20, pady=10)
next_button.pack()

# Start the GUI event loop
root.mainloop()
