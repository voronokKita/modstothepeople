# Mods To The People

![picture](azusa.jpg "Azusa")

Paradox makes wonderful games, that become even better with help of mod-creators community.<br>
In those cases when Steam Workshop & game launcher aren't accessible mod's installation become a boring monotonous job. For transition from ineffective hand labor to machine-working was written this script!

### Here is how it works

0. unpack your mods, give to the folders some simple names
1. put the mods and the script into /Paradox Interactive/your game folder/mod/
2. run terminal command python3 mttp.py
3. enter your game version

The script can be used for a cleanup, if you change set of mods then it removes old files & records.

## Detailed

You'll need Python 3 installed. It comes with Ubuntu by default and can be included in other OS as well. Check in the terminal:
> python3 --version<br>
You can get it here https://www.python.org/downloads/<br>
If you stuck then search "install python 3 in [your OS]", there are many detailed guides out there.

The script will definitely work on EU4 and HOI4, and probably on other games from this list:
> https://en.wikipedia.org/wiki/Paradox_Development_Studio#List_of_games_developed

You install mods in the folder "Paradox Interactive" that will be created after the first lunch of a game. On Windows and Mac it will be created in your "Documents" folder, on Linux in ~/.local/share/ of your home catalog.<br>
Normal order of mod installation in Europa Universalis IV by hands is this:
> 0. Copy descriptor.mod, that normally found inside a mod folder, into catalog<br>
/Paradox Interactive/Europa Universalis IV/mod/<br>
1. in the end of this descriptor file add a new line:<br>
path="path to the mod's folder"<br>
2. Next you enable the mod by making/editing this file<br>
/Paradox Interactive/Europa Universalis IV/dlc_load.json<br>
format of the file is this:<br>
{"disabled_dlcs" :[], "enabled_mods": ["mod/mod name 1.mod", "mod/mod name 2.mod", "mod/mod name 3.mod"]}

If this how it works in your case then the script must work regardless of OS and path to the "Paradox Interactive" folder!

#### Send me a couple of coins for a bun please
* PayPal: @kitavoronok
* bank: https://www.tinkoff.ru/rm/shaipov.nikita1/M7Qf620463

![picture](satania.jpg "no, you don't'")
