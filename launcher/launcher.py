import subprocess
from pathlib import Path

doom_path = Path("/mnt/i/Games/Games/GZDoom/UZDoom-4.14.3/uzdoom.exe")

def launch_profile(profile):

    subprocess.run([str(doom_path),
                    "-iwad",
                    profile["iwad"]])