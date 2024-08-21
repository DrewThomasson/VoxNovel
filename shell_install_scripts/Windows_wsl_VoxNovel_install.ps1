# Install Ubuntu in WSL
Write-Host "Installing Ubuntu in WSL..."
Start-Process powershell -ArgumentList "-Command wsl --install Ubuntu"

# Wait for 60 seconds
Start-Sleep -Seconds 5

# Run Ubuntu.sh command in Ubuntu
Write-Host "Running Ubuntu.sh in Ubuntu..."
Start-Process powershell -ArgumentList "-Command wsl -d Ubuntu -- bash -c 'wget -O - https://github.com/DrewThomasson/VoxNovel/raw/main/shell_install_scripts/Ubuntu-install.sh | bash'"


# Wait for 60 seconds
Start-Sleep -Seconds 5

# Open a new window that just reads 'done'
Write-Host "Opening a window that reads 'done'..."
Start-Process powershell -ArgumentList "-Command Write-Host 'done'; Read-Host -Prompt 'Press Enter to close'"
