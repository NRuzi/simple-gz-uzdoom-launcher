import subprocess
from pathlib import Path
from paths import PROFILES_DIR, MODS_DIR, doom_path

def launch_profile(profile):
    save_path = PROFILES_DIR / profile["name"] / "saves"
    save_path.mkdir(parents=True, exist_ok=True)

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