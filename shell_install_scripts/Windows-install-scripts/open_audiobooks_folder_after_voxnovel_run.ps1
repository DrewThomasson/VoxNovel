# Define the WSL base path
$homeDir = "\\wsl.localhost\Ubuntu\home"

# Get all user directories in the home folder
$userFolders = Get-ChildItem $homeDir | Where-Object { $_.PSIsContainer }

$pathFound = $false

foreach ($userFolder in $userFolders) {
    # Build the path to check
    $pathToCheck = Join-Path $userFolder.FullName "VoxNovel\output_audiobooks"
    
    # Check if the path exists
    if ([System.IO.Directory]::Exists($pathToCheck)) {
        Write-Output "WSL Path found: $pathToCheck"
        Start-Process explorer.exe $pathToCheck
        $pathFound = $true
        break
    }
}

if (-not $pathFound) {
    Write-Output "No 'VoxNovel\output_audiobooks' directory found in any user folder under $homeDir"
    Write-Output "You may need to manually navigate to: \\wsl.localhost\Ubuntu\home\USERNAME\VoxNovel\output_audiobooks"
    Write-Output "Where USERNAME is your WSL Ubuntu username."
    Write-Output "You can find all user directories at: \\wsl.localhost\Ubuntu\home\"
    Write-Output "The output audiobook files of VoxNovel are stored in the 'VoxNovel\output_audiobooks' directory."
}
