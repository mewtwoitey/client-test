# helper file to build and properly distribute the exe for testing
from pathlib import Path
import PyInstaller.__main__

import shutil
import os
import subprocess

from game.cards.card import Theme
input("This file will delete the release folder. press enter to continue")

release = input("Do you want to build it to be given out?") == "y"


PyInstaller.__main__.run([
    "main.py",
    "--collect-all",
    "textual",
    "--collect-all",
    "game.cards.fire",
    "--collect-all",
    "game.cards.wind",
    "--collect-all",
    "game.cards.earth",
    "--add-data",
    "card_imports.txt;.",
    "--add-data",
    "images;images",
    "--add-data",
    "ui/css;ui/css",
    "--onefile",
    "--noconfirm"
    
])

#card import file generator
themes = [t.name.lower() for t in Theme]
basedir = str(Path.cwd()) + "/game/cards/"

#go over the folders

imports = []


for theme in themes:
    for card_file in os.listdir(basedir+theme+"/"):
        if card_file.endswith("c.py"):
            imports.append(f"game.cards.{theme}.{card_file[:-3]}")
            
with open("card_imports.txt","w")as f:
    f.write("\n".join(imports))


dir_path = str(os.path.dirname(os.path.realpath(__file__)))
cmd= ["wt"]
if release:
    #release code here
    if os.path.exists("release"):
        shutil.rmtree("release")
    os.mkdir("release")



    shutil.copyfile("dist/main.exe","release/main.exe")



else:
    #developing

    for copy in range(4):
        location = rf"..\copy{copy+1}"
        shutil.copyfile("dist/main.exe",location+r"\main.exe")

        



