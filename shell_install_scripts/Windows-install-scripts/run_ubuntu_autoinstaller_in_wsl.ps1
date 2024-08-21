# Run Ubuntu.sh command in Ubuntu
Write-Host "Running Ubuntu.sh in Ubuntu..."
Start-Process powershell -ArgumentList "-Command wsl -d Ubuntu -- bash -c 'wget -O - https://github.com/DrewThomasson/VoxNovel/raw/main/shell_install_scripts/Ubuntu-install.sh | bash'"

