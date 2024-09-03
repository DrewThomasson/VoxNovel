To run this install script in one command without having to do anything else run this:


'yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu-install.sh | bash'


The test one is for if The nltk server isnt working and all the nltk moduals don't install this is grabbing from a backup i made of them from a docker image

'yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Test_Ubuntu_install.sh | bash'


### To install on windows run this command in powershell

`powershell -Command "Invoke-Expression (Invoke-WebRequest -Uri 'https://github.com/DrewThomasson/VoxNovel/raw/main/shell_install_scripts/Windows_wsl_VoxNovel_install.ps1').Content"`


### To install on Apple Silicone Mac run this command in your terminal

`bash <(curl -s https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Apple_silicone_VoxNovel_install.sh)
`

### To uninstall on Apple Silicone Mac run this command in your terminal

`bash <(curl -s https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/uninstall_VoxNovel_Mac.sh)
`

### To insall on Intel MAc run this command in your terminal
`bash <(curl -s https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Intel_Mac_Install_VoxNovel.sh)`
