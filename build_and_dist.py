# helper file to build and properly distribute the exe for testing
import PyInstaller.__main__

import shutil
import os
import subprocess
input("This file will delete the release folder. press enter to continue")

release = input("Do you want to build it to be given out?") == "y"


PyInstaller.__main__.run([
    "main.py",
    "--collect-all",
    "textual",
    "--collect-"
    "--onefile"
])
dir_path = str(os.path.dirname(os.path.realpath(__file__)))
cmd= ["wt"]
if release:
    #release code here
    if os.path.exists("release"):
        shutil.rmtree("release")
    os.mkdir("release")



    shutil.copyfile("dist/main.exe","release/main.exe")
    shutil.copytree("aseprite/","release/aseprite")
    shutil.copytree("ui/css/", "release/ui/css/")


else:
    #developing
    cmd= ["wt"]
    for copy in range(4):
        location = rf"..\copy{copy+1}"
        shutil.copyfile("dist/main.exe",location+r"\main.exe")

        cmd.extend([";", "nt" ,"-d", rf"{dir_path}\{location}"])
    subprocess.call(cmd)


