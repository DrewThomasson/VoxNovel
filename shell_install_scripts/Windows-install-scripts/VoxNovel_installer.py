import os
import subprocess
import requests
import tempfile
import tkinter as tk

# URLs of the PowerShell scripts and their descriptions
scripts = [
    {
        "url": "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/install_wsl.ps1",
        "description": "This step installs or checks if WSL (Windows Subsystem for Linux) is installed. Please ensure you have virtualization enabled in your system BIOS."
    },
    {
        "url": "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/run_ubuntu_autoinstaller_in_wsl.ps1",
        "description": "This step runs the auto-installer script in Ubuntu through WSL. Ensure that WSL is correctly set up before proceeding."
    },
    {
        "url": "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/create_desktop_shortcut.ps1",
        "description": "This step creates a desktop shortcut for VoxNovel. Ensure that you have completed the previous steps before running this script."
    }
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
        script_url = scripts[script_index]["url"]
        script_path = download_script(script_url)
        step_description = scripts[script_index]["description"]
        
        # Update the description label with the current step's description
        description_label.config(text=step_description)
        
        run_script(script_path)
        
        script_index += 1
        if script_index < len(scripts):
            next_button.config(text=f"Run Step {script_index + 1}")
        else:
            next_button.config(text="Finish", state="disabled")
            description_label.config(text="All steps completed!")
    else:
        root.quit()

# Set up the main application window
root = tk.Tk()
root.title("VoxNovel Installer")

script_index = 0

# Create a label for the warning message
warning_label = tk.Label(root, text="Make sure Virtualization is enabled in your system's BIOS, or this script will not work.", padx=20, pady=20, fg="red", font=("Helvetica", 12, "bold"))
warning_label.pack()

# Create a label for step descriptions
description_label = tk.Label(root, text="Press 'Next' to start the installation.", padx=20, pady=20)
description_label.pack()

# Create the 'Next' button
next_button = tk.Button(root, text="Run Step 1", command=on_next, padx=20, pady=10)
next_button.pack()

# Start the GUI event loop
root.mainloop()
