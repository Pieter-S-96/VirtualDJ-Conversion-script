import os
import re
from typing import OrderedDict
import xmltodict
from settings import *

class EditDataBaseFile():

    def __init__(self, XMLpath, MusicPath=None):
        self.XMLpath = XMLpath
        self.XMLname = "database.xml"
        self.XML = self.XMLpath + os.path.sep + self.XMLname

        self.MusicFolder = (MusicPath if MusicPath else MUSIC_FOLDER)

        self.rgx_filepath = r"FilePath=\"([^\"]+)\""
        self.rgx_changefiles = None # You can add a regex pattern here to change up some folders
        self.lines = "------------------------------------"

        self.DATA = None


    # remove any song metadata that doesn't come from the source folder
    def clean_up_library(self):
        print("Removing excessive metadata....")
        remove_indexes = []
        removedPaths = []
        X = 0
        
        for track in self.DATA["VirtualDJ_Database"]["Song"]:
            if (    re.search(r'Music\/Music\/Media', track['@FilePath'])
                    or re.search(r'\/Ableton\/Factory', track['@FilePath'])
                    or re.search(r'\/PioneerDJ\/', track['@FilePath'])
                    ):

                X += 1
                I = self.DATA["VirtualDJ_Database"]["Song"].index(track)
                remove_indexes.append(I)

                removedPaths.append(track['@FilePath'])

        with open(TEST_FILE + '_DELETE', 'w') as w:
            w.write('\n'.join(removedPaths))
        
        for index in sorted(remove_indexes, reverse=True):
            del self.DATA["VirtualDJ_Database"]["Song"][index]
        
        print(f"Removed {X} files")


    # Iterate over each track and replace the old file structure with the new one
    def replace_paths(self):
        print("\nConverting filepaths....")

        #Mind the separators!
        NEWSEP = ("\\" if "\\" in self.MusicFolder else "/")
        WRONGSEP = ("/" if '\\' in self.MusicFolder else "\\")

        print(f"OLD FOLDER NAME -- {OLD_FOLDER}")
        print(f"NEW FOLDER NAME -- {self.MusicFolder}")

        print('-')
        for track in self.DATA["VirtualDJ_Database"]["Song"]:
            filepath = track['@FilePath']
            if self.rgx_changefiles:
                if re.search(self.rgx_changefiles, filepath):
                    childpath = re.sub(self.rgx_changefiles, r'\1', filepath)
                    filepath = self.MusicFolder + childpath
                    filepath = rf'{filepath}'.replace(WRONGSEP, NEWSEP)
                
            if WRONGSEP in filepath:
                # print(f"Wrong separator found in --- {filepath}")
                filepath = rf'{filepath}'.replace(WRONGSEP, NEWSEP)
            
            I = self.DATA["VirtualDJ_Database"]["Song"].index(track)
            self.DATA["VirtualDJ_Database"]["Song"][I]['@FilePath'] = filepath

        print("\n....done converting!")
        return None


    # tidy up the library file so the structure is exactly the same
    def prep_xml(self, XML):
        # no tabs! single space indent
        XML = re.sub(r"\t", " ", XML)
        # empty all comments (gneheheh get rekt services)
        XML = re.sub(r"<Comment>[^\<]+<\/Comment>", "​<Comment></Comment>", XML)
        # Close off all components a bit neater like the normal XML
        XML = re.sub(r"><\/\w{2,5}>", " />", XML)
        # capitalize utf
        # encode apostrophes
        # add trailing newline
        return XML.replace("encoding=\"utf-8\"","encoding=\"UTF-8\"").replace("'", "&apos;") + '\n'


    # run database changes
    def run(self):
        print(self.lines)
        print("-- starting database run --\n")
        print("Opening & converting library....")
        with open(self.XML, 'r', encoding="utf8") as f:
            self.DATA = xmltodict.parse(f.read())

        print("Reading all filepaths....")
        filepaths = []
        sanitycheck = False # check if the old folder structure is found in any of the tracks
        for track in self.DATA["VirtualDJ_Database"]["Song"]:
            if not sanitycheck:
                if OLD_FOLDER in track['@FilePath']:
                    sanitycheck = True
            filepaths.append(track['@FilePath'])

        with open(TEST_FILE, 'w') as w:
            w.write('\n'.join(filepaths))
        
        if not sanitycheck:
            raise SystemExit("Old folder not found! did you already run the script?")
        print("Old filestructure found, continuing.....")

        print(f'...found a total of {len(self.DATA["VirtualDJ_Database"]["Song"])} tracks')
        self.clean_up_library()
        print(f'...{len(self.DATA["VirtualDJ_Database"]["Song"])} tracks left')

        self.replace_paths()

        print("Converting Library back to VirtualDJ format....")
        XML_new = xmltodict.unparse(self.DATA, pretty=True)

        with open(self.XML, 'w', encoding="utf8") as w:
            w.write(self.prep_xml(XML_new))

        print("\n....database done!")
        print(self.lines)