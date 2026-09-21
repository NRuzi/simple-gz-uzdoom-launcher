# Simple Doom Launcher

A simple launcher for GZDoom and UZDoom that lets you create profiles with their own saves, IWADs, and mods.

## Features

* Create Doom profiles (Currently only GZDoom and UZDoom supported)
* Support for multiple source port versions
* Create, edit, and delete profiles
* Select an IWAD for each profile
* Reorder mods before launching
* Save folders for each profile
* Automatically detects IWADS vs PWADS

## Requirements

* Python 3.12 or later if running from source
* GZDoom or UZDoom
* Any Doom IWAD

The packaged Windows release does not require Python to be installed.

## Installation

### Windows release

Download the latest release from the [Releases](../../releases) page and extract the folder.

### Running from source

Clone the repository:

```text
git clone https://github.com/NRuzi/simple-gz-uzdoom-launcher.git
cd simple-gz-uzdoom-launcher
```

For GUI:

```text
python scripts/gui.py
```

For CLI:

```text
python scripts/cli.py
```

Required folders will be generated on first run

## Setup

### 1. Install a source port

Place a GZDoom or UZDoom folder in the source_ports directory.

If the launcher is running, press the refresh button to load it into the dropdown menu.

### 2. Add your WADs

Place both your IWADs and PWADs in the wads directory.

The launcher should differentiate the two automatically, but hardcoded IWADs currently include:

* DOOM
* DOOM II
* TNT
* Plutonia
* Heretic
* Hexen
* Chex Quest
* Freedoom 1
* Freedoom 2

### 3. Create a profile

Use **Manage Profiles** to create a profile.

Select:

* A profile name
* An IWAD
* Any mods you want to use

Mods can be reordered to control their load order.

### Building from source

The executables can be built with PyInstaller:

```powershell
pyinstaller --clean --onefile --paths . scripts/gui.py
pyinstaller --clean --onefile --paths . scripts/cli.py
```

The resulting executables will be placed in the `dist` directory.

## Project Status

This is an early release and the project is still under development.

The launcher currently focuses on basic profile management and launching Doom source-port configurations.

## License

See [LICENSE](LICENSE) for license information.
