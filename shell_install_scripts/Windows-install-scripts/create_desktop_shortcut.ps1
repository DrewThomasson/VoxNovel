# Define the desktop shortcut path
$desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'VoxNovel.lnk')

# Define the target command
$targetPath = 'powershell.exe'
$arguments = '-Command "irm https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/open_VoxNovel_folder_windows.ps1 | iex; wsl -d Ubuntu -- bash -c ''yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu_run.sh | bash''; Invoke-Expression (Invoke-WebRequest -Uri ''https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/open_audiobooks_folder_after_voxnovel_run.ps1'').Content"'

# Define the path to the icon file
$iconPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'logo__1__GRD_icon.ico')

# Download the ICO file from the URL
Invoke-WebRequest -Uri 'https://github.com/DrewThomasson/VoxNovel/raw/main/readme_files/logo__1__GRD_icon.ico' -OutFile $iconPath

# Create a Shell COM object to create the shortcut
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($desktopPath)

# Set the properties for the shortcut
$shortcut.TargetPath = $targetPath
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = [System.IO.Path]::GetDirectoryName($targetPath)
$shortcut.IconLocation = "$iconPath,0"

# Save the shortcut
$shortcut.Save()
