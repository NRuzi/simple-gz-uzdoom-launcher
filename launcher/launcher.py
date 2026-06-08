import subprocess
import json
from pathlib import Path
from paths import PROFILES_DIR, MODS_DIR, PROJECT_ROOT

settings_file = PROJECT_ROOT / "settings.json"

def launch_profile(profile):
    save_path = PROFILES_DIR / profile["name"] / "saves"
    save_path.mkdir(parents=True, exist_ok=True)

    doom_path = load_doom_path()

    args = [
            str(doom_path),
            "-iwad",
            str(MODS_DIR / profile["iwad"]),
            "-savedir",
            str(save_path)
            ]
    
    for mod in profile["mods"]:
        args.extend([
            "-file",
            str(MODS_DIR / mod)
        ])

    subprocess.run(args)

def load_doom_path():
    if not settings_file.is_file():
        print("No settings found!")
        return

    with open(settings_file, "r") as file:
        settings = json.load(file)
    
    return settings["source_port"]