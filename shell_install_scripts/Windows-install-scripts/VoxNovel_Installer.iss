[Setup]
AppName=VoxNovel
AppVersion=1.0
DefaultDirName={pf}\VoxNovel
Compression=lzma
SolidCompression=yes
DisableFinishedPage=no

[Messages]
WelcomeLabel1=Welcome to the VoxNovel Graphical Installer
WelcomeLabel2=This is the graphical installer for VoxNovel.
Each step will run a separate PowerShell script that will launch a terminal window. [color=red]Make sure Virtualization is turned on in your computer's BIOS, or none of this will work.[/color]
Once the script is complete, the terminal window will automatically close so you can proceed to the next step.
Click [bold]Start Installation[/bold] to begin.

[Tasks]
Name: "closeterm1"; Description: "Close the terminal window after the first step"
Name: "closeterm2"; Description: "Close the terminal window after the second step"
Name: "closeterm3"; Description: "Close the terminal window after the third step"

[Files]
Source: "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/install_wsl.ps1"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/run_ubuntu_autoinstaller_in_wsl.ps1"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Windows-install-scripts/create_desktop_shortcut.ps1"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{tmp}\install_wsl.ps1"""; Description: "Install or check if WSL is installed"; Tasks: closeterm1
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{tmp}\run_ubuntu_autoinstaller_in_wsl.ps1"""; Description: "Run the auto installer in Ubuntu"; Tasks: closeterm2
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{tmp}\create_desktop_shortcut.ps1"""; Description: "Create a VoxNovel desktop shortcut"; Tasks: closeterm3

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssFinished then
  begin
    MsgBox('VoxNovel installation is complete. Enjoy!', mbInformation, MB_OK);
  end;
end;
