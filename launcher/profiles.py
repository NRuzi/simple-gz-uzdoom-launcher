from pathlib import Path
import json
from paths import PROFILES_DIR
from mods import list_mods, print_mod_list

PROFILES_DIR.mkdir(exist_ok=True)

def set_up_profile():
    profile = {
        "name": "",
        "iwad": "",
        "mods": [],
        "launch_args": []
    }

    profile["name"] = input("Enter a name for your profile\n")

    filename = PROFILES_DIR / f"{profile['name']}.json"
    if filename.is_file():
        print("A profile with that name already exists")
        return

    # Eventually add logic to check mod folder for present iwads, once GUI is setup, add an option to manually choose an iwad from file explorer
    while True:
        iwad_choice = input("Please select an iwad:\n[1] DOOM\n[2] DOOM 2\n")
        match iwad_choice:
            case "1":
                profile["iwad"] = "DOOM.WAD"
                break
            case "2":
                profile["iwad"] = "DOOM2.WAD"
                break
            case _:
                print("Invalid selection")
    
    # Once GUI is setup, scan the mods folder and give a checklist for mod selection
    mods = list_mods()
    mod_selection = []

    while True:
        print("Please select your mods:\n")
        print_mod_list(mods, mod_selection)
        print("[n] Next")
        mod_choice = input()

        if mod_choice == "n" or mod_choice == "N":
            profile["mods"] = mod_selection
            break
        
        else:
            if mods:
                try:
                    selected_mod = mods[int(mod_choice) - 1]
                    
                    if selected_mod in mod_selection:
                        mod_selection.remove(selected_mod)
                    else:
                        mod_selection.append(selected_mod)

                except (ValueError, IndexError):
                    print("Invalid selection")

    # Potentially give launch argument options, or just leave a text box input

    return profile
     
def save_profile(profile):
    new_profile_directory = PROFILES_DIR / f"{profile['name']}"
    filename = new_profile_directory / "profile.json"

    new_profile_directory.mkdir(exist_ok=True, parents=True)

    with open(filename, "w") as file:
        json.dump(profile, file, indent=4)

def create_profile():
    profile = set_up_profile()
    if profile == None:
        return
    save_profile(profile)
    print(f"\nCreated profile: {profile['name']}\n")

def load_profile(name):
    filename = PROFILES_DIR / f"{name}" / "profile.json"

    if not filename.is_file():
        print("Profile not found")
        return

    with open(filename, "r") as file:
        return json.load(file)
    
def list_profiles():
    profiles = []

    for folder in PROFILES_DIR.iterdir():
        if folder.is_dir() and (folder / "profile.json").is_file():
            profiles.append(folder.name)

    return profiles