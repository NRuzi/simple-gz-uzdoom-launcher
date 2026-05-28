from pathlib import Path
import json

profile_path = Path("./profiles")
profile_path.mkdir(exist_ok=True)

def set_up_profile():
    profile = {
        "name": "",
        "iwad": "",
        "mods": [],
        "launch_args": []
    }

    profile["name"] = input("Enter a name for your profile\n")

    filename = profile_path / f"{profile['name']}.json"
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

    # Potentially give launch argument options, or just leave a text box input

    return profile
     
def save_profile(profile):
    filename = profile_path / f"{profile['name']}.json"

    with open(filename, "w") as file:
        json.dump(profile, file, indent=4)

def create_profile():
    profile = set_up_profile()
    if profile == None:
        return
    save_profile(profile)
    print(f"Created profile: {profile['name']}")

def load_profile(name):
    filename = profile_path / f"{name}.json"

    if not filename.is_file():
        print("Profile not found")
        return

    with open(filename, "r") as file:
        return json.load(file)
    
def list_profiles():
    return [file.stem for file in profile_path.glob("*.json")]