# Unreal Launcher for Linux

A no-nonsense PyQt6 launcher for managing Unreal Engine 4/5 projects on Linux. Scans your home directory for engine installs and .uproject files, handles the messy GUID registration that Epic doesn't properly document for source builds, and gives you a dark mode UI that won't burn your retinas at 2 AM.

## Why This Exists
If you've built UE from source on Linux, you've probably hit the "Failed to locate Unreal Engine associated with the project file" error. The "fix" involves manually editing `~/.config/Epic/UnrealEngine/Install.ini` and jamming a GUID into your .uproject file. This tool automates that nonsense.

Also, I got tired of navigating to engine directories manually. This finds your installs and projects automatically.

## Features
* **Auto-discovery:** Recursively scans for UE4/UE5 engine roots and .uproject files (respects .git, node_modules, Saved, etc. — skips the junk)
* **Engine Association Fix:** One-click patch to register source-built engines with the Epic launcher system
* **Project Generation:** Runs GenerateProjectFiles.sh without leaving the UI
* **Dark Theme:** JetBrains Mono + gold accents. Looks decent, doesn't blind you.

## Requirements
```bash
sudo apt install python3-pyqt6
```
That's it. No pip hell, no venvs, no 500MB of dependencies.

## Usage
```bash
chmod +x ue_launch.py
./ue_launch.py
```
Or just `python3 ue_launch.py` if you're into that.

## What It Actually Does

### Engine Detection
Looks for Engine/Binaries/Linux/UnrealEditor or the UE4 equivalent, parses Engine/Build/Build.version to figure out what you're running. Stops crawling at depth 5 so it doesn't spend forever in your home folder.

### The GUID Fix (Linux Source Builds)
Epic's Linux support for source builds is... spotty. The launcher expects engines to be registered in `~/.config/Epic/UnrealEngine/Install.ini` with a GUID mapping to the install path. This tool:
1. Reads existing registrations
2. Generates a new GUID if your engine isn't registered
3. Writes it to Install.ini
4. Patches your .uproject to use that GUID

This is the correct way to fix the association error. Not symlinking random directories, not editing ~/.bashrc, not sacrificing goats.

### Project Generation
Runs the shell script with -project= -game -engine flags. Captures stdout/stderr so you can see what broke without opening a terminal.

## Roadmap
* **Packaging / Building:** Cooking and packaging projects directly from the launcher — planned for a future update.

## Limitations
* **Linux only.** If you're on Windows, use the actual Epic Launcher.
* **Assumes standard source build layout.** If you moved Engine/ somewhere weird, it won't find it.

## License
Do whatever. If it breaks your project, that's on you. Back up your .uproject files before running the association fix (though it does preserve the old value in the log).
