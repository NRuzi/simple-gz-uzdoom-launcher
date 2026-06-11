import shutil
from pathlib import Path
from profiles import list_profiles, load_profile, build_profile, save_profile
from launcher import launch_profile
from settings import load_settings, search_source_ports, set_source_port, source_port_is_configured
from mods import list_mods, list_iwads
from paths import SOURCE_PORT_DIR, PROFILES_DIR


def main():
    source_port_check()

    while True:

        selected_profile = main_menu_choice()
        
        profile_json = load_profile(selected_profile)
        launch_profile(profile_json)
        break

def print_main_menu(profiles):

    print("\nSimple Doom Launcher:\n")

    for i, profile in enumerate(profiles, start=1):
            print(f"[{i}] {profile}")

    print("[n] New Profile")
    print("[e] Edit Profile")
    print("[d] Delete Profile")
    print("[s] Settings")
    print("")

def main_menu_choice():

    while True:
        profiles = list_profiles()

        print_main_menu(profiles)
    
        choice = input("Select an option: ")

        if choice.lower() == "n":
            set_up_profile()
            continue

        elif choice.lower() == "e":
            edit_menu_choice(profiles)
            continue

        elif choice.lower() == "d":
            delete_menu_choice(profiles)
            continue
        
        elif choice.lower() == "s":
             source_port_menu()
             continue

        else:
            if profiles:
                try:
                    selected_profile = profiles[int(choice) - 1]
                    return selected_profile

                except (ValueError, IndexError):
                    print("Invalid selection")

def edit_menu_choice(profiles):
    print("\nSelect a profile to edit:\n")

    for i, profile in enumerate(profiles, start=1):
            print(f"[{i}] {profile}")
    
    print("[b] Back to main menu")

    edit_choice = input()

    if edit_choice.lower() == "b":
         return
    
    if profiles:
         try:
              selected_profile = profiles[int(edit_choice) - 1]
              edit_profile_menu(selected_profile)
         
         except (ValueError, IndexError):
              print("Invalid selection")


def delete_menu_choice(profiles):
    print("\nSelect a profile to delete:\n")

    for i, profile in enumerate(profiles, start=1):
            print(f"[{i}] {profile}")
    
    print("[b] Back to main menu")

    delete_choice = input()

    if delete_choice.lower() == "b":
         return
    
    if profiles:
         try:
              selected_profile = profiles[int(delete_choice) - 1]
              delete_profile_menu(selected_profile)
         
         except (ValueError, IndexError):
              print("Invalid selection")

def source_port_check():
     if not source_port_is_configured():
          print("No source port detected!")
          source_port_menu()

def source_port_menu():
     settings = load_settings()
     source_ports = search_source_ports()

     while True:
        print("\nSet a copy of GZDoom / UZDoom")

        for i, source_port in enumerate(source_ports, start=1):
            relative_path = source_port.relative_to(SOURCE_PORT_DIR)
            print(f"[{i}] {relative_path}")

        print("[r] Rescan source ports folder")
        print("[m] Enter manually")

        port_choice = input()

        if port_choice.lower() == "r":
             source_ports = search_source_ports()
             continue

        if port_choice.lower() == "m":
            manual_port_entry(settings)
            return
        
        if source_ports:
            try:
                selected_port = source_ports[int(port_choice) - 1]
                set_source_port(settings, selected_port)
                return
            
            except (ValueError, IndexError):
                print("Invalid selection")

def manual_port_entry(settings):
     while True:
         print("Please paste the path to your GZDoom / UZDoom executable:")

         port_path = Path(input().strip())

         if not port_path.exists():
              print("File does not exist!")
              continue
         
         if not port_path.is_file():
              print("Path is not a file!")
              continue
         
         if port_path.name.lower() not in ["gzdoom.exe", "uzdoom.exe"]:
              print("Not a supported source port executable!")
              continue
         
         set_source_port(settings, port_path)
         print("Source path set!")
         return

def set_iwad_menu(profile):
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

def set_mods_menu(profile):
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

def delete_profile_menu(profile):
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

def edit_profile_menu(profile_name):
    profile = load_profile(profile_name)

    while True:
        print("What would you like to edit?\n")
        print("[1] iwad choice")
        print("[2] mod selection")

        edit_choice = input()

        match (edit_choice):
            case "1":
                set_iwad_menu(profile)
                break
            case "2":
                set_mods_menu(profile)
                break
            case _:
                print("Invalid selection\n")
    
    save_profile(profile)

def set_up_profile():

    name = input("Enter a name for your profile\n")

    profile = build_profile(name)

    set_iwad_menu(profile)

    set_mods_menu(profile)

    save_profile(profile)

    print(f"Created profile: f{profile['name']}")

    return

def print_mod_list(mod_list, selected):

    for i, mod in enumerate(mod_list, start=1):
            marker = "X" if mod in selected else " "
            print(f"[{marker}] [{i}] {mod}")

def print_iwad_list(iwad_list):
     
     for i, iwad in enumerate(iwad_list, start=1):
          print(f"[{i}] {iwad}")

main()