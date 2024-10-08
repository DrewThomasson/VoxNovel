# Function to prompt user to press Enter to continue
function WaitForUserInput {
    param (
        [string]$message
    )
    
    Write-Host $message
    Read-Host -Prompt 'Press Enter to continue'
}

# Install Ubuntu in WSL
Write-Host "Installing Ubuntu in WSL..."
Start-Process powershell -ArgumentList "-Command wsl --install Ubuntu"

# Prompt user to press Enter to continue
WaitForUserInput -message "Ubuntu installation initiated. Please press Enter when the installation is complete."

# Run Ubuntu.sh command in Ubuntu
Write-Host "Running Ubuntu.sh in Ubuntu..."
Start-Process powershell -ArgumentList "-Command wsl -d Ubuntu -- bash -c 'wget -O - https://github.com/DrewThomasson/VoxNovel/raw/main/shell_install_scripts/Ubuntu-install.sh | bash'"

# Prompt user to press Enter to continue
WaitForUserInput -message "Ubuntu setup is running. Please press Enter when this process is complete."

# Define the desktop shortcut path
$desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'VoxNovel.lnk')

# Define the target command
$targetPath = 'powershell.exe'
$arguments = '-Command wsl -d Ubuntu -- bash -c ''yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu_run.sh | bash'''

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

# Open a new window that just reads 'done'
Write-Host "Opening a window that reads 'done'..."
Start-Process powershell -ArgumentList "-Command Write-Host 'done'; Read-Host -Prompt 'Press Enter to close'"
