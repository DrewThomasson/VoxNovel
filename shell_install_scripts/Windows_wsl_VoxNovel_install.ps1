# Install Ubuntu in WSL
Write-Host "Installing Ubuntu in WSL..."
#Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-2004 -OutFile ubuntu.appx -UseBasicParsing
#Add-AppxPackage -Path ubuntu.appx
# Run WSL installation for Ubuntu
wsl --install Ubuntu

# Wait for 60 seconds
Start-Sleep -Seconds 60

