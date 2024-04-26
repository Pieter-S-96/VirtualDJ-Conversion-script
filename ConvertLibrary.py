import os
import re
import shutil
from pathlib import Path
from tkinter import filedialog

from settings import *
from Classes.database import EditDataBaseFile
from Classes.virtualFolder import EditVirtualFolder

if __name__ == '__main__':
    DialogText = "Please select the location of the VirtualDJ folder" \
        " (When you run this script you should have downloaded/uploaded it somewhere)"

    DialogTextMusic = "Please select the location of your music folder"

    filePath = filedialog.askdirectory(mustexist=True, title=DialogText)

    musicPath = None # defaults to settings path
    if not MUSIC_FOLDER:
        musicPath = filedialog.askdirectory(mustexist=True, title=DialogTextMusic)
        if musicPath[-1] != '\\':
            musicPath += '\\'

    if not Path(filePath).exists():
        raise NameError("Folder doesn't exist!")

    # back up the old metadata
    shutil.make_archive("VirtualDJ_BACKUP", "zip", filePath)

    db = EditDataBaseFile(filePath, musicPath)
    db.run()

    folder = EditVirtualFolder(filePath, musicPath)
    folder.run()

    print("\n\n--- ALL DONE ---")
