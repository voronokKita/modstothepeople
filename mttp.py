#! python3
""" (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
v1 january 2022
v2 march 2022
v3 april 2022"""
import re
import sys
import json
import pathlib


PATTERN = re.compile(r'\d+\.\d+(\.\d+)?')
MAIN_DIR = pathlib.Path.cwd()
DLC_LOAD = MAIN_DIR.parent / "dlc_load.json"
GAME_VERSION = ""


class Mod:
    def __init__(self, name, folder, descriptor, data=None):
        self.name = name
        self.folder = folder
        self.descriptor = descriptor
        self.data = data

    def save(self, target_dir):
        new_descriptor = target_dir / f"{self.name}.mod"
        with open(new_descriptor, 'w') as file:
            file.write(self.data)
        print(f"saved {self}")

    def __str__(self):
        return f"{self.name}"


def main():
    if MAIN_DIR.parent.parent.stem != "Paradox Interactive":
        print("Run the script in the /Documents/Paradox Interactive/your game folder/mod/",
              f"Current working directory is {MAIN_DIR}",
              "Continue anyway? [y/n]:", sep="\n", end=" ")
        answer = input().lower().strip()
        if not answer in ["y", "yes"]:
            sys.exit(1)

    elif len(sys.argv) > 1:
        if not PATTERN.fullmatch(sys.argv[1]):
            print(f"Enter a game version in a format like 'python3 {sys.argv[0]} 3.2.1'")
            sys.exit(2)
        else:
            global GAME_VERSION
            GAME_VERSION = f'supported_version="{sys.argv[1]}"'

    try:
        mods = paths_handler()
        mods, json_data = processing(mods)
        writer(mods, json_data)
    except OSError:
        print("Error read/write data. Don't have permissions?")
        sys.exit(3)
    except Exception as error:
        print("Unknown error occurred. Details:",
              "-" * 10, f"{error}", "-" * 10,
              "You may contact with me and I'll try to fix it!", sep="\n")
        sys.exit(4)
    else:
        print("Done.")
        sys.exit(0)


def paths_handler():
    print("directory:", MAIN_DIR)
    mods_dirs = [item for item in MAIN_DIR.iterdir() if item.is_dir()]

    mods = []
    for directory in mods_dirs:
        descriptor = [item for item in directory.iterdir() if item.name.endswith( ('.mod', '.mod.old') )]
        if not descriptor:
            print(f"mod {directory.stem} doesn't have a descriptor file; skipped")
            continue
        else:
            descriptor = descriptor[0]
        mod = Mod(directory.stem, directory, descriptor)
        mods.append(mod)

    if not mods:
        print("no mods found.")
        sys.exit(0)
    else:
        print(len(mods), "mods found")

    return mods


def processing(mods):
    enabled_mods = []
    data = ""
    for mod in mods:
        with open(mod.descriptor, 'r', encoding='utf-8') as file:
            for line in file:
                if GAME_VERSION and "supported_version" in line:
                    line = GAME_VERSION + "\n"
                data += line
        data += f'\npath="{mod.folder}"\n'
        mod.data = data

        enabled_mods.append(f"mod/{mod.name}.mod")

    json_data = {'disabled_dlcs': [], 'enabled_mods': enabled_mods}
    return mods, json_data


def writer(mods, json_data):
    [item.unlink() for item in MAIN_DIR.iterdir() if item.name.endswith('.mod')]

    for mod in mods:
        if mod.descriptor.name.endswith('.mod'):
            mod.descriptor.rename(f"{mod.descriptor}.old")

    for mod in mods:
        mod.save(MAIN_DIR)

    with open(DLC_LOAD, 'w') as file:
        json.dump(json_data, file)


if __name__ == '__main__':
    main()
