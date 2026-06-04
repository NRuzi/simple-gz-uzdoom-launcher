from pathlib import Path
from paths import MODS_DIR

MODS_DIR.mkdir(exist_ok=True)

VALID_EXTENSIONS = {".wad", ".pk3", ".deh"}
KNOWN_IWADS = {
    "DOOM.WAD",
    "DOOM2.WAD",
    "PLUTONIA.WAD",
    "TNT.WAD",
    "HERETIC.WAD",
    "HEXEN.WAD",
    "CHEX.WAD"
}

def list_mods():
    mods = []

    for file in MODS_DIR.iterdir():
        if not file.is_file():
            continue
        
        if file.suffix.lower() in [".pk3", ".deh"]:
            mods.append(file.name)

        elif (file.suffix.lower() == ".wad" 
              and file.name.upper() not in KNOWN_IWADS 
              and get_wad_type(file) == "PWAD"):
            mods.append(file.name)
    
    return mods
    

def print_mod_list(mod_list, selected):

    for i, mod in enumerate(mod_list, start=1):
            marker = "X" if mod in selected else " "
            print(f"[{marker}] [{i}] {mod}")

def get_wad_type(path):
    try:
        with open(path, "rb") as file:
            return file.read(4).decode("ascii")
    except (OSError, UnicodeDecodeError):
        return None

def list_iwads():
    iwads = []

    for file in MODS_DIR.iterdir():
        if not file.is_file():
             continue

        if file.name.upper() in KNOWN_IWADS:
              iwads.append(file.name)

        elif file.suffix.lower() == ".wad":
              if get_wad_type(file) == "IWAD":
                   iwads.append(file.name)
    
    return iwads

def print_iwad_list(iwad_list):
     
     for i, iwad in enumerate(iwad_list, start=1):
          print(f"[{i}] {iwad}")