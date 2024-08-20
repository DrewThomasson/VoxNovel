# Define variables
$desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'VoxNovel.lnk')
$scriptPath = "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu-install.sh"
$logoUrl = "https://github.com/DrewThomasson/VoxNovel/raw/6f49c6a8b36927c987b1d628ff3e9c1afcb04dab/readme_files/logo.jpeg"
$shortcutName = "VoxNovel"

# Create the shortcut
Write-Host "Creating desktop shortcut..."
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($desktopPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -NoNewWindow -Command wsl -d Ubuntu -- bash -c 'wget -O - $scriptPath | bash'"
$Shortcut.IconLocation = "powershell.exe,0" # Default PowerShell icon
$Shortcut.Save()

# Download the logo
Write-Host "Downloading logo..."
$logoPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'logo.jpeg')
Invoke-WebRequest -Uri $logoUrl -OutFile $logoPath

# Set the icon for the shortcut
Write-Host "Setting icon for the shortcut..."
$Shortcut.IconLocation = $logoPath
$Shortcut.Save()

# Ensure WSL is set up and not prompting interactively
Write-Host "Ensuring WSL is set up and not prompting interactively..."
wsl --list --verbose

Write-Host "Process completed."
