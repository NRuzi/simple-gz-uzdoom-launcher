from pathlib import Path
import json
from paths import PROJECT_ROOT, SOURCE_PORT_DIR

SOURCE_PORT_DIR.mkdir(exist_ok=True)
settings_file = PROJECT_ROOT / "settings.json"

def build_settings():
    settings = {
        "source_port" : ""
    }

    save_settings(settings)

def load_settings():
    if not settings_file.is_file():
        build_settings()

    with open(settings_file, "r") as file:
        return json.load(file)

def save_settings(settings):
    with open(settings_file, "w") as file:
        json.dump(settings, file, indent=4)

def source_port_is_configured():
    settings = load_settings()

    return settings["source_port"] != ""

def search_source_ports():
    source_ports = []

    for file in SOURCE_PORT_DIR.rglob("*.exe"):
        if file.name.lower() in ["gzdoom.exe", "uzdoom.exe"]:
            source_ports.append(file)
    
    return source_ports

def set_source_port(settings, source_port):
    settings["source_port"] = str(source_port)
    save_settings(settings)
    return
    
