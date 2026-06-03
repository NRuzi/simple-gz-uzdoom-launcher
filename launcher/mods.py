from pathlib import Path
from paths import MODS_DIR

MODS_DIR.mkdir(exist_ok=True)

VALID_EXTENSIONS = {".wad", ".pk3", ".deh"}

def list_mods():
    return [
        file.name
        for file in MODS_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in VALID_EXTENSIONS
    ]

def print_mod_list(mod_list, selected):

    for i, mod in enumerate(mod_list, start=1):
            marker = "X" if mod in selected else " "
            print(f"[{marker}] [{i}] {mod}")

