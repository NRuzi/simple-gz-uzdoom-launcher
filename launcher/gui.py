import tkinter as tk
from tkinter import ttk

from profiles import list_profiles, load_profile
from launcher import launch_profile
from settings import source_port_is_configured, search_source_ports, load_settings, set_source_port

from paths import SOURCE_PORT_DIR

def update_launch_button():
    profile_selected = profile_dropdown.current() != -1

    if profile_selected and source_port_is_configured():
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

def launch_selected_profile():
    profile_index = profile_dropdown.current()
    profile_name = profiles[profile_index]
    profile = load_profile(profile_name)

    launch_profile(profile)

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