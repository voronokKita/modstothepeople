#! python3
""" (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
v1 january 2022
v2 march 2022
v3 april 2022 """
import re
import sys
import json
import pathlib
import argparse
import traceback



MAIN_DIR = pathlib.Path.cwd()
DLC_LOAD = MAIN_DIR.parent / 'dlc_load.json'
GAME_VERSION = None
RENAME = False
VERSION = re.compile(r'\d+\.\d+(\.\d+)?')
JSON_PATTERN = re.compile(r'(\[)(.*)(\])(.+)(enabled_mods)', re.DOTALL | re.I)  #?

class NoMods(Exception): pass

class Mod:
    def __init__(self, name, folder, descriptor, data=None):
        self.name = name
        self.folder = folder
        self.descriptor = descriptor
        self.data = data

    def save(self):
        inner_desctiptor = self.folder / 'descriptor.mod'
        with open(inner_desctiptor, 'w', encoding='utf-8') as file:
            file.write(self.data)

        outer_descriptor = self.folder.parent / f'{self.name}.mod'
        with open(outer_descriptor, 'w', encoding='utf-8') as file:
            file.write(self.data)

    def __repr__(self):
        return self.name


def main(args):
    global RENAME
    RENAME = args.rename

    if args.version:
        global GAME_VERSION
        GAME_VERSION = f'supported_version="{args.version}"'

    try:
        mods = paths_handler()
        mods, json_data = processing(mods)
        writer(mods, json_data)

    except NoMods:
        print('no mods found.')
        sys.exit(0)

    except OSError:
        print("Error read/write data. Don't have permissions?")
        sys.exit(1)

    except Exception:
        print('Unknown error occurred. Details:',
              '-' * 10, traceback.format_exc(), '-' * 10,
              "You may contact with me and I'll try to fix it!", sep='\n')
        sys.exit(2)

    else:
        print('Done.')
        sys.exit(0)


def paths_handler():
    print('directory:', MAIN_DIR)
    mods_dirs = [item for item in MAIN_DIR.iterdir() if item.is_dir()]

    mods = []
    for directory in mods_dirs:
        descriptor = [item for item in directory.iterdir()
                      if item.is_file() and item.name.endswith('.mod.original')]

        if not descriptor:
            descriptor = [item for item in directory.iterdir()
                          if item.is_file() and item.name.endswith('.mod')]

        if not descriptor:
            print(f"mod {directory.stem} doesn't have " \
                  "a descriptor file; skipped")
            continue

        else:
            descriptor = descriptor[0]

        mod = Mod(directory.stem, directory, descriptor)
        mods.append(mod)

    if not mods: raise NoMods
    else: print(len(mods), 'mods found')

    mods.sort(key=lambda mod: mod.name)
    return mods


def processing(mods):
    enabled_mods = []
    for mod in mods:
        data = ''
        with open(mod.descriptor, 'r', encoding='utf-8') as file:
            for line in file:
                if GAME_VERSION and 'supported_version=' in line:
                    line = GAME_VERSION + '\n'
                elif RENAME and 'name=' in line:
                    line = f'name="{mod.name}"\n'

                data += line

        data += f'\npath="{mod.folder}"\n'
        mod.data = data

        enabled_mods.append(f'mod/{mod.name}.mod')

    dlcs = []
    if DLC_LOAD.exists():
        try:
            data = DLC_LOAD.read_text(encoding='utf-8')
            raw_dlcs = JSON_PATTERN.findall(data)[0][1]
            if raw_dlcs:
                for item in raw_dlcs.split(','):
                    dlc = item.replace('"', '').strip()
                    if dlc: dlcs.append(dlc)
        except Exception: pass

    json_data = {'disabled_dlcs': dlcs, 'enabled_mods': enabled_mods}

    return mods, json_data


def writer(mods, json_data):
    for mod in mods:
        if not mod.descriptor.name.endswith('.mod.original'):
            mod.descriptor.rename(f"{mod.descriptor}.original")

    [item.unlink() for item in MAIN_DIR.iterdir()
     if item.is_file() and item.name.endswith('.mod')]

    for mod in mods:
        mod.save()
        print(f'saved {mod}')

    with open(DLC_LOAD, 'w', encoding='utf-8') as file:
        json.dump(json_data, file)


if __name__ == '__main__':
    if MAIN_DIR.parent.parent.stem != 'Paradox Interactive':
        p = pathlib.Path('Documents', 'Paradox Interactive', 'your game folder', 'mod')
        print(f'Run the script in the {p}',
              f'Current working directory is {MAIN_DIR}',
              'Continue anyway? [y/n]:', sep='\n', end=' ')

        answer = input().lower().strip()
        if not answer in ['y', 'yes']:
            sys.exit(1)

    def game_version_pattern(line):
        if not line: return ''
        elif not VERSION.fullmatch(line):
            s = f"\nEnter a game version in a format like 'python3 {sys.argv[0]} 3.2.1'"
            raise argparse.ArgumentTypeError(s)
        else: return line

    parser = argparse.ArgumentParser()
    parser.add_argument('version', nargs='?', default='', type=game_version_pattern,
                        help='rewrite a game version')
    parser.add_argument('-r', '--rename', action='store_true', default=False,
                        help='rename mods to match their folders')
    args = parser.parse_args()

    main(args)
