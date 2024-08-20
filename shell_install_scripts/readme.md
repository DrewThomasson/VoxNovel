To run this install script in one command without having to do anything else run this:


'yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu-install.sh | bash'


The test one is for if The nltk server isnt working and all the nltk moduals don't install this is grabbing from a backup i made of them from a docker image

'yes | wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Test_Ubuntu_install.sh | bash'


### To install on windows run this command

`Start-Process powershell -ArgumentList "-Command wsl -d Ubuntu -- bash -c 'wget -O - https://raw.githubusercontent.com/DrewThomasson/VoxNovel/main/shell_install_scripts/Ubuntu-install.sh | bash'" -NoNewWindow -Wait`
