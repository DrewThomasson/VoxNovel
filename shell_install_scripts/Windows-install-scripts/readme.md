## Building the Executable

To convert the Python script into a standalone executable, follow these steps:

1. **Install PyInstaller**:

   ```bash
   pip install pyinstaller
   ```

2. **Generate the Executable**:

   Run the following command to create the `.exe` file:

   ```bash
   pyinstaller --onefile --windowed VoxNovel_installer.py
   ```

3. **Locate the Output**:

   The resulting executable will be found in the `dist` directory:

   ```
   dist/VoxNovel_installer.exe
   ```












## Depricated do not use
To create the graphical installer for VoxNovel using the Inno Setup script I provided, you would need to follow these steps:

1. Download and install Inno Setup from the official website: https://jrsoftware.org/isinfo.php

2. Create a new text file and copy the Inno Setup script I provided into it. Save the file with a `.iss` extension, for example, `VoxNovel_Installer.iss`.

3. Open the Inno Setup Compiler (it should have been installed with Inno Setup).

4. In the Inno Setup Compiler, go to File > Open and select the `VoxNovel_Installer.iss` file you just created.

5. Click the "Compile" button to generate the installer executable.

The compiled installer executable will be saved in the same directory as your `.iss` file. You can then distribute this executable to your users, and they can run it to install VoxNovel on their Windows machines.

The Inno Setup script I provided should create a graphical installer with the following steps:

1. Welcome screen with a "Start Installation" button
2. Running the first PowerShell script with a "Next" button
3. Running the second PowerShell script with a "Next" button
4. Running the third PowerShell script with a "Next" button
5. Final "Done" screen
