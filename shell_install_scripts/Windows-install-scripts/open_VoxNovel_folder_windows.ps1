# Define the WSL base path
$homeDir = "\\wsl.localhost\Ubuntu\home"

# Get the first user directory in the home folder
$userFolder = Get-ChildItem $homeDir | Where-Object { $_.PSIsContainer } | Select-Object -First 1

if ($userFolder -ne $null) {
    # Build the path to open
    $pathToOpen = Join-Path $userFolder.FullName "VoxNovel"

    # Display a pop-up message to the user
    [System.Windows.MessageBox]::Show("Please place your ebook file in the 'VoxNovel' folder so that VoxNovel can access it.", "VoxNovel Notice", "OK", "Information")
    
    # Display the path to verify it is correct
    Write-Output "WSL Path to open: $pathToOpen"
    
    # Open the path directly in Windows Explorer
    if ([System.IO.Directory]::Exists($pathToOpen)) {
        Start-Process explorer.exe $pathToOpen
    } else {
        Write-Output "The path does not exist: $pathToOpen"
        Write-Output "You may need to manually navigate to: \\wsl.localhost\Ubuntu\home\USERNAME\VoxNovel\output_audiobooks"
        Write-Output "Where USERNAME is your WSL Ubuntu username."
        Write-Output "You can find all user directories at: \\wsl.localhost\Ubuntu\home\"
        Write-Output "The output audiobook files of VoxNovel are stored in the 'VoxNovel\output_audiobooks' directory."
    }
} else {
    Write-Output "No user directory found under $homeDir"
    Write-Output "You may need to manually navigate to: \\wsl.localhost\Ubuntu\home\USERNAME\VoxNovel\output_audiobooks"
    Write-Output "Where USERNAME is your WSL Ubuntu username."
    Write-Output "You can find all user directories at: \\wsl.localhost\Ubuntu\home\"
    Write-Output "The output audiobook files of VoxNovel are stored in the 'VoxNovel\output_audiobooks' directory."
}
