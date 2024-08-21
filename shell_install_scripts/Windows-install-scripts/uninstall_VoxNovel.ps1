# Remove VoxNovel Desktop shortcut
Write-Host "Removing VoxNovel Desktop Shortcut..."

# Define the desktop shortcut path
$desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'VoxNovel.lnk')

# Check if the shortcut exists and delete it
if (Test-Path $desktopPath) {
    Remove-Item $desktopPath
    Write-Host "VoxNovel.lnk has been deleted from the desktop."
} else {
    Write-Host "VoxNovel.lnk not found on the desktop."
}

# Uninstall Ubuntu in WSL
Write-Host "Uninstalling Ubuntu in WSL..."
Start-Process powershell -ArgumentList "-Command wsl --unregister Ubuntu"
Write-Host "Done!"

