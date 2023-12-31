# SCARAB: Encrypted notetaking that runs on the terminal.

## Files included:
#### `getexe.cmd`: Given the existing scrb.py file, and pyinstaller is installed in your system, this generates an .exe file for the application that can be easily ran, even without the Python intepreter installed.
#### `icon.ico`: An .ico file for the logo/icon of the app.
#### `scrb.py`: The python code for the app.
#### `scrb.exe`: the executable file for the app. If lost, running getexe.cmd will bring this back.

## Use as a standard app
Scarab can be used like a normal PC application by double clicking on the .exe file and entering the commands. You can move it to anywhere you like and create desktop shortcuts to it. Scarab is entirely text-based and does not have a GUI. Type 'help' while within the app to see the full list of commands.

## Run in terminal
Like all .exe files, setting the folder as a system variable path, would enable you to run the program immediately via the Command Prompt or Powershell just by entering the name of the .exe file, without changin the target directory:
1. Enter the start menu, search for 'env'
2. Click on 'Edit the system environment variables'
3. Click on 'Environment Variables'
4. File 'System Variables' and double-click on 'Path'.
5. Add the path to the folder that contains this `scrb.exe` file. If you downloaded Scarab recently and did not move things around, this folder SHOULD be located in your Downloads folder: `C:\Users\<yourname>\Downloads`

You can now immediately execute Scarab commands directly into terminal. For example, typing `scrb add` into Command Prompt would immediately add a note. Same goes for all other commands, just remember to type `scrb` in front. This enables you to access Scarab functions quickly in situations where your terminal is always open, such as when you are coding.

## How it works
All notes are stored in a Python dictionary data type, which is exactly the same as a JSON format. The dictionary will then be converted to string format, which will be encrypted using the `cryptography.fernet` Python package. 

There is a default encryption key (shown in the Python code) if the notes are not passcode-protected. If the notes are passcode-protected, the encryption key will be generated using the passcode as a seed, meaning that the notes will be completely inaccessible without the passcode. To do this, the `SHA-256` hash algorithm is used to generate a unique encryption key for almost every choice of passcode.

The encrypted data is then written into a file called `scarabData`, located in `C:\Users\<yourname>\Local\AppData\Scarab`. Another file, `scarabStatus`, is used to tell if the data is password protected or not. DO NOT modify these files.

Fetching data would be the reverse - reading the `scarabData` file, decrypting it using the encryption key, the evaluating the string contents as a dictionary.