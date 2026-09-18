import tkinter as tk
from tkinter import ttk, messagebox
import shutil

from profiles import list_profiles, load_profile, save_profile, profile_exists
from launcher import launch_profile
from settings import source_port_is_configured, search_source_ports, load_settings, set_source_port
from mods import list_iwads, list_mods

from paths import SOURCE_PORT_DIR, PROFILES_DIR

def update_launch_button():
    profile_selected = profile_dropdown.current() != -1

    if profile_selected and source_port_is_configured() and source_port_is_valid():
        launch_button.config(state="normal")
    else:
        launch_button.config(state="disabled")

def profile_selected(event):
    update_launch_button()

def source_port_selected(event):
    index = source_port_dropdown.current()
    selected_port = source_ports[index]

    settings = load_settings()
    set_source_port(settings, selected_port)

    update_launch_button()

def rescan_source_ports():
    global source_ports

    source_ports = search_source_ports()

    source_port_dropdown["values"] = [
        str(port.relative_to(SOURCE_PORT_DIR))
        for port in source_ports
    ]

def source_port_is_valid():
    source_ports = search_source_ports()
    settings = load_settings()
    configured_port = settings["source_port"]

    return configured_port in source_ports

def launch_selected_profile():
    profile_index = profile_dropdown.current()
    profile_name = profiles[profile_index]
    profile = load_profile(profile_name)

    launch_profile(profile)

def open_profile_manager():
    window = tk.Toplevel(root)
    window.title("Profile Manager")
    window.geometry("400x300")

    profiles = list_profiles()

    profile_list = tk.Listbox(window)

    for profile in profiles:
        profile_list.insert(tk.END, profile)

    profile_list.pack()

    def refresh_profile_list():
        profiles.clear()
        profiles.extend(list_profiles())

        profile_list.delete(0, tk.END)

        for profile in profiles:
            profile_list.insert(tk.END, profile)

        refresh_main_profile_dropdown()

    create_button = tk.Button(
        window,
        text="Create",
        command=lambda: open_profile_editor(None, refresh_profile_list)
    )
    create_button.pack()

    def edit_selected_profile():
        selection = profile_list.curselection()

        if not selection:
            return

        index = selection[0]
        profile_name = profiles[index]

        profile = load_profile(profile_name)

        open_profile_editor(profile, refresh_profile_list)

    edit_button = tk.Button(
        window,
        text="Edit",
        command=edit_selected_profile
    )
    edit_button.pack()

    def delete_profile():
        selection = profile_list.curselection()

        if not selection:
            return

        index = selection[0]
        profile_name = profiles[index]
        profile_path = PROFILES_DIR / profile_name

        if not profile_path.is_dir():
                messagebox.showerror("Delete Error","Profile not found")
                return

        confirmation = messagebox.askyesno("Delete Profile", f"Are you sure you want to delete {profile_name}?")

        if not confirmation:
            return

        try:
            shutil.rmtree(profile_path)
        except OSError as error:
            messagebox.showerror("Delete Error", str(error))
            return

        profiles.pop(index)
        profile_list.delete(index)
        refresh_main_profile_dropdown()

    delete_button = tk.Button(
        window,
        text="Delete",
        command=delete_profile
    )
    delete_button.pack()

def open_profile_editor(profile, on_save=None):
    new_profile = profile is None

    window = tk.Toplevel(root)
    window.title("Create Profile" if new_profile else "Edit Profile")
    window.geometry("400x300")

    #New profile logic
    if new_profile:
        name_entry = ttk.Entry(window)
        name_entry.pack()

        profile = {
        "name": "",
        "iwad": "",
        "mods": [],
        "launch_args": []
    }


    #iwad selection logic
    iwads = list_iwads()
    iwad_var = tk.StringVar()

    if profile["iwad"]:
        iwad_var.set(profile["iwad"])

    iwad_menu = ttk.Combobox(
        window,
        textvariable=iwad_var,
        values=iwads,
        state="readonly"
    )
    iwad_menu.pack()

    def get_selected_iwad():
        index = iwad_menu.current()

        if index == -1:
            return None
        
        return iwad_var.get()

    #avilable/selected mod list logic
    mods = list_mods()
    selected_mods = profile["mods"].copy()
    available_mods = [mod for mod in mods if mod not in selected_mods]

    available_list = tk.Listbox(
        window,
        selectmode=tk.SINGLE
    )
    available_list.pack()

    selected_list = tk.Listbox(
        window,
        selectmode=tk.SINGLE,
    )
    selected_list.pack()

    for mod in available_mods:
        available_list.insert(tk.END, mod)

    for mod in selected_mods:
        selected_list.insert(tk.END, mod)

    #button logic
    def select_mod():
        selection = available_list.curselection()
    
        if not selection:
            return
    
        index = selection[0]
        mod = available_mods.pop(index)
    
        selected_mods.append(mod)
    
        available_list.delete(index)
        selected_list.insert(tk.END, mod)

    select_button = tk.Button(
        window,
        text="->",
        state="normal",
        command=select_mod
    )
    select_button.pack()

    def deselect_mod():
        selection = selected_list.curselection()

        if not selection:
            return

        index = selection[0]
        mod = selected_mods.pop(index)

        available_mods.insert(0, mod)

        selected_list.delete(index)
        available_list.insert(0, mod)

    deselect_button = tk.Button(
        window,
        text="<-",
        state="normal",
        command=deselect_mod
    )
    deselect_button.pack()

    def move_mod_up():
        selection = selected_list.curselection()

        if not selection:
            return

        index = selection[0]

        if index == 0:
            return

        selected_mods[index], selected_mods[index - 1] = selected_mods[index - 1], selected_mods[index]

        selected_list.delete(0, tk.END)

        for mod in selected_mods:
            selected_list.insert(tk.END, mod)

        selected_list.selection_set(index - 1)

    up_button = tk.Button(
        window,
        text="↑",
        state="normal",
        command=move_mod_up
    )
    up_button.pack()

    def move_mod_down():
        selection = selected_list.curselection()

        if not selection:
            return

        index = selection[0]

        if index >= len(selected_mods) - 1:
            return

        selected_mods[index], selected_mods[index + 1] = selected_mods[index + 1], selected_mods[index]

        selected_list.delete(0, tk.END)

        for mod in selected_mods:
            selected_list.insert(tk.END, mod)

        selected_list.selection_set(index + 1)

    down_button = tk.Button(
        window,
        text="↓",
        state="normal",
        command=move_mod_down
    )
    down_button.pack()

    def save_button_click():
        if new_profile:
            name = name_entry.get().strip()

            if name == "":
                messagebox.showerror("Invalid Profile", "Please enter a profile name.")
                return

            if profile_exists(name):
                messagebox.showerror("Invalid Profile", "Profile already exists")
                return

            profile["name"] = name
        
        iwad = get_selected_iwad()

        if iwad is None:
            messagebox.showerror("Invalid Profile", "Please select an IWAD")
            return

        profile["iwad"] = iwad
        profile["mods"] = selected_mods

        save_profile(profile)

        if on_save:
            on_save()

        window.destroy()

    save_button = tk.Button(
        window,
        text="Save",
        state="normal",
        command=save_button_click
    )
    save_button.pack()

    cancel_button = tk.Button(
        window,
        text="Cancel",
        command=window.destroy
    )
    cancel_button.pack()

def refresh_main_profile_dropdown():
    profiles.clear()
    profiles.extend(list_profiles())
    profile_dropdown["values"] = profiles

    if profile_selection.get() not in profiles:
        profile_selection.set("")

    update_launch_button()

root = tk.Tk()
root.title("Doom Launcher")
root.geometry("500x400")

source_ports = search_source_ports()
source_port_var = tk.StringVar()

source_port_dropdown = ttk.Combobox(
    root,
    textvariable=source_port_var,
    values=[str(port.relative_to(SOURCE_PORT_DIR)) for port in source_ports],
    state="readonly"
)

source_port_dropdown.pack()

source_port_refresh = tk.Button(
    root,
    text="Refresh Source Ports",
    state="normal",
    command=rescan_source_ports
)

source_port_refresh.pack()

settings = load_settings()
configured_port = settings["source_port"]

if configured_port in source_ports:
    source_port_dropdown.current(source_ports.index(configured_port))
else:
    source_port_var.set("")

for index, port in enumerate(source_ports):
    if str(port) == configured_port:
        source_port_dropdown.current(index)
        break

profiles = list_profiles()

profile_selection = tk.StringVar()

profile_dropdown = ttk.Combobox(
    root,
    textvariable=profile_selection,
    values=profiles,
    state="readonly"
)

profile_dropdown.pack()

profile_button = tk.Button(
    root,
    text="Manage Profiles",
    command=open_profile_manager
)

profile_button.pack()

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