# VirtualDJ Conversion script from Linux/MacOS to Windows

Script for converting VirtualDJ metadata to Windows
- Author: Pieter Speelman
- Python 3.9 recommended

## Installation
- configure *settings.py*:
```python
from os.path import sep
MUSIC_FOLDER = "C:\\path\\to\\directory\\"
OLD_FOLDER = "/old/path/to/directory/"
VDJ_FOLDER_NAME_OLD = "Old folder name"
VDJ_FOLDER_NAME_NEW = "New folder name"
TEST_FILE = "tests" + sep + "TESTFILE"
```
- MUSIC_FOLDER -> location of your track files
- OLD_FOLDER -> where the virtualDJ XML's think the tracks are (check VirtualDJ -> database.xml)
- VDJ_FOLDER_NAME_OLD -> old name for VDJ folder with music (check VirtualDJ -> Folders -> XXXXX.subfolders)
- VDJ_FOLDER_NAME_NEW = name of your new folder
- TEST_FILE = path config for test files location if you want to test

## Script execution
- dont forget to backup settings/DB!
- run python file <code>ConvertLibrary.py</code>
- a dialog will ask to select the virtualDJ folder - this concerns the metadata folder. usually somewhere in your documents
- after a succesful run - a backup ZIP will also have been created

## Steps after running the script
- open VirtualDJ. Check if the folders are configured right
- check if the settings are not overwritten! settings_backup.xml can revert those for you