from profiles import list_profiles, create_profile, load_profile, edit_profile, delete_profile
from launcher import launch_profile


def main():
    
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
    print("")

def main_menu_choice():

    while True:
        profiles = list_profiles()

        print_main_menu(profiles)
    
        choice = input("Select an option: ")

        if choice.lower() == "n":
            create_profile()
            #profiles = list_profiles()
            continue

        elif choice.lower() == "e":
            edit_menu_choice(profiles)
            continue

        elif choice.lower() == "d":
            delete_menu_choice(profiles)
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

main()