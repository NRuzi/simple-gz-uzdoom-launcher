from profiles import list_profiles, create_profile, load_profile
from launcher import launch_profile


def main():
    
    print("\nSimple Doom Launcher:\n")

    while True:
        profiles = list_profiles()

        selected_profile = main_menu_choice(profiles)
        
        profile_json = load_profile(selected_profile)
        launch_profile(profile_json)
        break

def print_main_menu(profiles):

    for i, profile in enumerate(profiles, start=1):
            print(f"[{i}] {profile}")

    print("[n] New Profile\n")

def main_menu_choice(profiles):

    while True:
        print_main_menu(profiles)
    
        choice = input("Select an option: ")

        if choice == "n" or choice == "N":
            create_profile()
            profiles = list_profiles()
            continue
        
        else:
            if profiles:
                try:
                    selected_profile = profiles[int(choice) - 1]
                    return selected_profile

                except (ValueError, IndexError):
                    print("Invalid selection")

main()