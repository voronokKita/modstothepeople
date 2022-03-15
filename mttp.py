#! python3
""" (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
v1 winter 2022
v2 spring 2022
TODO remote id"""
import re
import sys
import json
import random
import pathlib
import collections

PATTERN = re.compile(r'\d+\.\d+(\.\d+)?')
MAIN_DIR = pathlib.Path.cwd()
DLC_LOAD = MAIN_DIR.parent / "dlc_load.json"
GAME_VERSION = "*.*.*"


def main():
    if len(sys.argv) > 1:
        if not PATTERN.fullmatch(sys.argv[1]):
            print(f"Enter a game version in a format like 'python3 {sys.argv[0]} 3.2.1'")
            sys.exit(1)
        else:
            global GAME_VERSION
            GAME_VERSION = sys.argv[1]

    try:
        mods_dirs = paths_handler()
        mods_data, json_data = processing(mods_dirs)
        writer(mods_data, json_data, mods_dirs)

    except OSError:
        print("Error read/write data. Don't have permissions?")
        sys.exit(2)
    else:
        print("Done.")
        sys.exit(0)


def paths_handler():
    print("directory:", MAIN_DIR)

    mods_dirs = [item for item in MAIN_DIR.iterdir() if item.is_dir()]
    if len(mods_dirs) == 0:
        print("No mods found.")
        sys.exit(0)
    else:
        print(len(mods_dirs), "mods found:")
        print(*[f"{item.stem}" for item in mods_dirs], sep=', ')

    return mods_dirs


def processing(mods_dirs):
    mods_data = {}
    enabled_mods = []
    supported_version = f'supported_version="{GAME_VERSION}"'
    for mod_path in mods_dirs:
        name = f'name="{mod_path.stem}"'
        path = f'path="{mod_path}"'
        thumbnail = get_picture(mod_path)

        mods_data[mod_path] = f"{name}\n{supported_version}\n{thumbnail}\n{path}\n"

        enabled_mods.append(f"mod/{mod_path.stem}.mod")

    json_data = {'disabled_dlcs': [], 'enabled_mods': enabled_mods}
    return mods_data, json_data


def get_picture(mod_path):
    thumbnail = ""
    for item in mod_path.iterdir():
        if item.is_file() and "thumbnail" in item.name:
            thumbnail = item.name
    if not thumbnail:
        pics = [item.name for item in mod_path.iterdir() if item.name.endswith( ('.jpg', '.jpeg', '.png') )]
        thumbnail = random.choice(pics) if len(pics) > 0 else ""
    return f'picture="{thumbnail}"'


def writer(mods_data, json_data, mods_dirs):
    [item.unlink() for item in MAIN_DIR.iterdir() if item.name.endswith('.mod')]
    for mod in mods_dirs:
        [resource.rename(f"{resource}.old") for resource in mod.iterdir() if resource.name.endswith('.mod')]

    for mod in mods_data:
        descriptor_file = MAIN_DIR / f"{mod.stem}.mod"
        with open(descriptor_file, 'w') as f:
            f.write(mods_data[mod])

    with open(DLC_LOAD, 'w') as f:
        json.dump(json_data, f)


if __name__ == '__main__':
    main()
