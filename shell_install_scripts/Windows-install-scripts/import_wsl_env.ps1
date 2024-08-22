# Define variables
$downloadUrl = "https://huggingface.co/drewThomasson/VoxNovel_WSL_ENV/resolve/main/Windows_WSL_VoxNovel.tar?download=true"
$tarFilePath = "$env:USERPROFILE\Downloads\Windows_WSL_VoxNovel.tar"
$extractPath = "C:\WSL\VoxNovel"

# Download the tar file
Invoke-WebRequest -Uri $downloadUrl -OutFile $tarFilePath

# Create the extraction directory if it doesn't exist
if (-not (Test-Path $extractPath)) {
    New-Item -Path $extractPath -ItemType Directory
}

# Extract the tar file using tar command
tar -xvf $tarFilePath -C $extractPath

# Optionally, remove the tar file after extraction
Remove-Item $tarFilePath

Write-Output "WSL environment 'VoxNovel' installed at $extractPath"
