# Mods To The People

![picture](azusa.jpg "Azusa")

###### ([руководство на русском](https://github.com/voronokKita/modstothepeople/blob/master/%D0%9F%D0%A0%D0%9E%D0%A7%D0%A2%D0%98%20%D0%9C%D0%95%D0%9D%D0%AF%20%D0%BD%D0%B0%20%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC.md))

Paradox makes wonderful games, that become even better with help of mod-creators community.<br>
In those cases when Steam Workshop isn't accessible, or you don't want to use it, mods installation becomes a boring monotonous job. This script will help you to transition from inefficient manual labor to machine-working.

### Here is how it works

0. unpack your mods, (give to the folders some good names if you want)
1. put the mods and the script into '/Documents/Paradox Interactive/your game folder/mod/'
2. run in this filder a terminal command 'python3 mttp.py'
3. or 'python3 mttp.py [your game version] to overwrite it'

If you change your set of mods then it'll cleanup old files & records.

## Detailed

You'll need Python 3 installed. It comes with Ubuntu by default and can be included in other OS as well. Check in the terminal:

> python3 --version

You can get it here https://www.python.org/downloads/<br>
If you stuck then search "install python 3 in [your OS]", there are many detailed guides out there.

The script will definitely work on EU4 and HOI4, and probably on other games from this list:

> https://en.wikipedia.org/wiki/Paradox_Development_Studio#List_of_games_developed

You install mods in the 'Paradox Interactive' folder, that will be created after the first lunch of a game. On Windows and Mac it will be created in your 'Documents' folder, on Linux in '~/.local/share/' of your home catalog.<br>
Normal order of mod installation on Europa Universalis IV by hands is:

0. Copy descriptor.mod, that normally found inside a mod folder, into the<br>
/Paradox Interactive/Europa Universalis IV/mod/<br>
1. in the end of this descriptor file add a new line<br>
path="path to the mod's folder"<br>
2. Next you enable the mod by making/editing file<br>
/Paradox Interactive/Europa Universalis IV/dlc_load.json<br>
format of the file is this<br>
{"disabled_dlcs" :[], "enabled_mods": ["mod/mod name 1.mod", "mod/mod name 2.mod", "mod/mod name 3.mod"]}

If this how it works in your case then the script must work, regardless of your OS and a path to the 'Paradox Interactive' folder!

#### I'm new to GitHub and don't know how to download

![guide](howto.jpg "how to download")
