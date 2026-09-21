from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROFILES_DIR = PROJECT_ROOT / "user_profiles"
MODS_DIR = PROJECT_ROOT / "wads"
SOURCE_PORT_DIR = PROJECT_ROOT / "source_ports"