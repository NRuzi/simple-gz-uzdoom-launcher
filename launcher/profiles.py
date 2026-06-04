from pathlib import Path
import json, shutil
from paths import PROFILES_DIR
from mods import list_mods, print_mod_list, list_iwads, print_iwad_list

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

    set_iwad(profile)
        
    # Once GUI is setup, scan the mods folder and give a checklist for mod selection

    set_mods(profile)

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

def edit_profile(profile_name):
    profile = load_profile(profile_name)

    while True:
        print("What would you like to edit?\n")
        print("[1] iwad choice")
        print("[2] mod selection")

        edit_choice = input()

        match (edit_choice):
            case "1":
                set_iwad(profile)
                break
            case "2":
                set_mods(profile)
                break
            case _:
                print("Invalid selection\n")
    
    save_profile(profile)

def set_iwad(profile):
    while True:
        iwads = list_iwads()

        if iwads:
            print("Please select an iwad:\n")
            print_iwad_list(iwads)
            iwad_choice = input()

            try:
                selected_iwad = iwads[int(iwad_choice) - 1]
                profile["iwad"] = selected_iwad
                return
            
            except (ValueError, IndexError):
                print("Invalid selection")
        
        else:
            print("No iwads detected!")
            return

def set_mods(profile):
    mods = list_mods()
    mod_selection = profile["mods"]

    while True:
        print("Please select your mods:\n")
        print_mod_list(mods, mod_selection)
        print("[n] Next")
        mod_choice = input()

        if mod_choice == "n" or mod_choice == "N":
            profile["mods"] = mod_selection
            return
        
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

def delete_profile(profile):
    profile_path = PROFILES_DIR / profile

    if not profile_path.is_dir():
        print("Profile not found")
        return
    
    confirmation = input(f"Delete profile '{profile}' and its contents? (y/n): ")

    if confirmation.lower() != "y":
        print("Deletion cancelled")
        return
    
    shutil.rmtree(profile_path)
    print(f"Deleted profile: {profile}")