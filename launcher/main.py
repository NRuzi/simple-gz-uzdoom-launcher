from pathlib import Path
from profiles import list_profiles, create_profile, load_profile, edit_profile, delete_profile
from launcher import launch_profile
from settings import load_settings, save_settings, search_source_ports, set_source_port, source_port_is_configured
from paths import SOURCE_PORT_DIR


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
            create_profile()
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
              edit_profile(selected_profile)
         
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
              delete_profile(selected_profile)
         
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

main()