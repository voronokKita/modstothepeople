#! python3
""" (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
v1 winter 2022 """
import re
import sys
import json
import pathlib
import collections

PATTERN = re.compile(r'\d+\.\d+(\.\d+)?')
Handler = collections.namedtuple("Handler", "mods_dirs, dlc_load, game_version")


def main():
    try:
        handler = paths_handler()
        mods, json_data = processing(handler)
        writer(handler, mods, json_data)

    except OSError:
        print("Error read/write data. Don't have permissions?")
        sys.exit(1)
    else:
        print("Done.")
        sys.exit(0)


def paths_handler():
    main_dir = pathlib.Path.cwd()
    print("directory:", main_dir)

    mods_dirs = [item for item in main_dir.iterdir() if not item.is_file()]
    if len(mods_dirs) == 0:
        print("No mods found.")
        sys.exit(0)
    else:
        print(len(mods_dirs), "mods found")
        print(*[f"{item.stem}" for item in mods_dirs], sep=', ')

    dlc_load = main_dir.parent / "dlc_load.json"

    print("Enter game version | Введите версию игры:")
    game_version = "None"
    while not PATTERN.fullmatch(game_version):
        game_version = input().strip()

    return Handler(mods_dirs, dlc_load, game_version)


def processing(datas):
    mods = {}
    mods_list = []
    supported_version = f'supported_version="{datas.game_version}"'
    for mod_path in datas.mods_dirs:
        name = f'name="{mod_path.stem}"'
        path = f'path="{mod_path}"'
        mods[mod_path] = f"{name}\n{supported_version}\n{path}\n"

        mods_list.append(f"mod/{mod_path.stem}.mod")

    json_data = {'disabled_dlcs': [], 'enabled_mods': mods_list}
    return mods, json_data


def writer(handler, mods, json_data):
    [item.unlink() for item in pathlib.Path.cwd().iterdir() if item.name.endswith('.mod')]

    for item in mods:
        descriptor = pathlib.Path.cwd() / f"{item.stem}.mod"
        with open(descriptor, 'w') as f:
            f.write(mods[item])

    with open(handler.dlc_load, 'w') as f:
            json.dump(json_data, f)


if __name__ == '__main__':
    main()
