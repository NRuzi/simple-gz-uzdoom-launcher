from profiles import list_profiles, create_profile, load_profile
from launcher import launch_profile


def main():
    profiles = list_profiles()
    
    print("Simple Doom Launcher:\n")

    while True:
        for i, profile in enumerate(profiles, start=1):
            print(f"[{i}] {profile}")

        print("[n] New Profile\n")
    
        choice = input("Select an option: ")

        if choice == "n" or choice == "N":
            create_profile()
            profiles = list_profiles()
            continue
        
        else:
            if profiles:
                try:
                    selected_profile = profiles[int(choice) - 1]
                    break

                except (ValueError, IndexError):
                    print("Invalid selection")
    
    profile_json = load_profile(selected_profile)
    launch_profile(profile_json)

main()