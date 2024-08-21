[Setup]
AppName=VoxNovel
AppVersion=1.0
DefaultDirName={pf}\VoxNovel
DefaultGroupName=VoxNovel
OutputBaseFilename=VoxNovel_installer
Compression=lzma
SolidCompression=yes
SetupIconFile="C:\Users\super\Desktop\logo__1__GRD_icon.ico"

[Run]
Filename: "powershell.exe"; Parameters: "-Command Invoke-Expression (Invoke-WebRequest -Uri 'https://github.com/DrewThomasson/VoxNovel/raw/main/shell_install_scripts/Windows_wsl_VoxNovel_install.ps1' -UseBasicParsing).Content"; Flags: runhidden

[Code]
function InitializeSetup(): Boolean;
begin
  MsgBox('Please ensure that virtualization is enabled in your BIOS settings before continuing with the installation. The installation will not work without it.', mbInformation, MB_OK);
  Result := True;
end;