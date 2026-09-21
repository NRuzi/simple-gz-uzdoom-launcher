import json
from paths import PROFILES_DIR

PROFILES_DIR.mkdir(exist_ok=True)

def build_profile(name):
    profile = {
        "name": "",
        "iwad": "",
        "mods": [],
        "launch_args": []
    }

    if profile_exists(name):
        raise ValueError("Profile already exists")

    else:
        profile["name"] = name

    return profile
     
def save_profile(profile):
    new_profile_directory = PROFILES_DIR / f"{profile['name']}"
    filename = new_profile_directory / "profile.json"

    new_profile_directory.mkdir(exist_ok=True, parents=True)

    with open(filename, "w") as file:
        json.dump(profile, file, indent=4)

def load_profile(name):
    filename = PROFILES_DIR / f"{name}" / "profile.json"

    if not filename.is_file():
        raise FileNotFoundError("Profile not found!")

    with open(filename, "r") as file:
        return json.load(file)
    
def list_profiles():
    profiles = []

    for folder in PROFILES_DIR.iterdir():
        if folder.is_dir() and (folder / "profile.json").is_file():
            profiles.append(folder.name)

    return sorted(profiles)

def profile_exists(name):
    filename = PROFILES_DIR / str(name) / f"profile.json"

    return filename.is_file()