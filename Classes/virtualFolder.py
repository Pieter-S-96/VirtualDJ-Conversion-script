import os
import re
from settings import *
from shutil import rmtree

class EditVirtualFolder():

    def __init__(self, FolderPath, MusicPath=None):
        self.TopFolderPath = FolderPath
        self.TopFolderName = "Folders"
        self.TopFolder = self.TopFolderPath + os.path.sep + self.TopFolderName

        self.MusicFolder = (MusicPath if MusicPath else MUSIC_FOLDER)

        self.FolderNameOld = VDJ_FOLDER_NAME_OLD
        self.FolderOld = self.TopFolder + os.path.sep + self.FolderNameOld
        self.FolderNameNew = VDJ_FOLDER_NAME_NEW
        self.FolderNew = self.TopFolder + os.path.sep + self.FolderNameNew
        self.vfolders = []

        self.rgx_checkpath = r"path=\"([^\"]+)\""
        self.rgx_changefiles = r"^.+?/((Par|Mio)[^\"]+)\" idx=\"\d+\"  />"
        self.lines = "------------------------------------"

        self.DATA = None
        self.NEWDATA = None


    def search_folders(self, path):
        print(f"recursively checking -- {path}")
        for item in os.listdir(path):
            if '.subfolders' in item:
                self.search_folders(path + os.path.sep + item)
            if '.vdjfolder' in item:
                print(f"\t -- found folder: {item.replace('.vdjfolder','')}")
                self.vfolders.append(path + os.path.sep + item)
        

    # Iterate over each track in a folder and replace the old file structure with the new one
    def replace_paths(self, vfolder):
        #Mind the separators!
        NEWSEP = ("\\" if "\\" in self.MusicFolder else "/")
        WRONGSEP = ("/" if '\\' in self.MusicFolder else "\\")

        name = vfolder.split(NEWSEP)[-1].replace(".vdjfolder","")
        print(f"Altering Folder: {name:30}.... ", end='')

        with open(vfolder, 'r') as f:
            self.DATA = f.readlines()
        self.NEWDATA = [None] * len(self.DATA)

        for index, line in enumerate(self.DATA):
            if re.search(self.rgx_checkpath, line):
                childpath = None
                try:
                    childpath = re.findall(self.rgx_changefiles, line)[0][0]
                    childpath = childpath.replace(WRONGSEP, NEWSEP)
                except:
                    SystemError(f"Something is going wrong in the {name} playlist, line {index}:\n\n{line}")
                
                if not childpath:
                    continue # don't change metadata, something went wrong
                
                newpath = f'path="{self.MusicFolder}{childpath}"'
                cleanpath = re.sub(self.rgx_checkpath, "path=''", line)
                fixedline = cleanpath.replace("path=''", newpath)
                self.NEWDATA[index] = fixedline
        
            if self.NEWDATA[index]:
                self.DATA[index] = self.NEWDATA[index]

        newparent = self.FolderNew + '.subfolders'
        newname = 'DJG - ' + name + '.vdjfolder'

        with open(newparent + os.path.sep + newname, 'w') as f:
            f.write(''.join(self.DATA))
        print(f"new name: {self.FolderNameNew} / {newname.replace('.vdjfolder','')}")


    # run virtual folder changes
    def run(self):
        print(self.lines)
        print("-- starting V-folder conversion --\n")
        print("Recursively finding V-folders....")

        print(f"OLD FOLDER NAME -- {OLD_FOLDER}")
        print(f"NEW FOLDER NAME -- {self.MusicFolder}\n")

        # nothing in the main folder please
        if os.path.exists(self.FolderOld + '.vdjfolder'):
            os.remove(self.FolderOld + '.vdjfolder')
        
        # make a new parent folder
        if not os.path.exists(self.FolderNew + '.subfolders'):
            os.mkdir(self.FolderNew + '.subfolders')

        # recursive searching
        self.search_folders(self.FolderOld + '.subfolders')

        # fixing the filepaths
        for vfolder in self.vfolders:
            self.replace_paths(vfolder)

        # removing old names
        if os.path.exists(self.FolderOld + '.subfolders'):
            rmtree(self.FolderOld + '.subfolders')
        
        print("\n....vfolders done!")
        print(self.lines)
