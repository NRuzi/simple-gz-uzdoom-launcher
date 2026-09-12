import tkinter as tk
from tkinter import ttk

from profiles import list_profiles, load_profile
from launcher import launch_profile

def profile_selected(event):
    launch_button.config(state="normal")

def launch_selected_profile():
    profile_index = profile_dropdown.current()
    profile_name = profiles[profile_index]
    profile = load_profile(profile_name)

    launch_profile(profile)

root = tk.Tk()
root.title("Doom Launcher")
root.geometry("500x400")

profiles = list_profiles()

profile_selection = tk.StringVar()

profile_dropdown = ttk.Combobox(
    root,
    textvariable=profile_selection,
    values=profiles,
    state="readonly"
)

profile_dropdown.pack()

launch_button = tk.Button(
    root,
    text="Launch Doom",
    state="disabled",
    command=launch_selected_profile
)

launch_button.pack()

profile_dropdown.bind(
    "<<ComboboxSelected>>",
    profile_selected
)

root.mainloop()