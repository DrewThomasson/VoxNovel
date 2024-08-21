import tkinter as tk
from tkinter import messagebox
import subprocess
import requests
from PIL import Image, ImageTk
import io

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def run_ps1_script():
    # Download the PowerShell script
    ps1_script_url = "https://github.com/DrewThomasson/VoxNovel/raw/main/shell_install_scripts/Windows-install-scripts/uninstall_VoxNovel.ps1"
    ps1_script_path = "uninstall_VoxNovel.ps1"
    download_file(ps1_script_url, ps1_script_path)

    # Run the PowerShell script
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_script_path], check=True)
        messagebox.showinfo("Success", "VoxNovel has been uninstalled successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to uninstall VoxNovel.")

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("VoxNovel Uninstaller")
    root.geometry("300x200")

    # Load and set the icon
    icon_url = "https://github.com/DrewThomasson/VoxNovel/raw/main/readme_files/logo__1__GRD_icon.ico"
    response = requests.get(icon_url)
    icon_data = io.BytesIO(response.content)
    icon_image = Image.open(icon_data)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)

    # Create a label
    label = tk.Label(root, text="Click to uninstall VoxNovel", pady=20)
    label.pack()

    # Create an uninstall button
    uninstall_button = tk.Button(root, text="Uninstall", command=run_ps1_script)
    uninstall_button.pack()

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    create_gui()
