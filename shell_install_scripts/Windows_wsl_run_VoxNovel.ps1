# Run WSL with specified commands
$wslCommand = @"
wsl -d Ubuntu bash -c "conda activate VoxNovel && cd ~ && cd VoxNovel && python gui_run.py"
"@

Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `$wslCommand" -NoNewWindow -Wait
