# Py Builder

[cite_start]A Tkinter-based GUI utility designed to automate the conversion of Python scripts into standalone executables using PyInstaller. [cite: 1]

---

## Features

* [cite_start]**Automatic Script Detection**: Scans the directory in real-time for .py and .pyw files. [cite: 14, 15]
* [cite_start]**Smart Dependency Management**: Uses Abstract Syntax Trees to find imports and attempts to install missing modules via pip. [cite: 6, 21, 22]
* **Adaptive Build Modes**: 
    * [cite_start]**Console Mode**: Applied to .py files. [cite: 22]
    * [cite_start]**Windowed Mode**: Applied to .pyw files using the --noconsole flag. [cite: 22]
* [cite_start]**Theme Support**: Includes Dark and Light modes with settings that persist in a JSON file. [cite: 2, 8, 9, 17]
* [cite_start]**Workspace Cleanup**: Optionally removes build, dist, and .spec files after the build process. [cite: 4, 5, 27]
* [cite_start]**Real-Time Logging**: Displays the full PyInstaller output directly within the application scrolled text area. [cite: 14, 23]

---

## Requirements

* [cite_start]**Python 3.x**. [cite: 1]
* [cite_start]**PyInstaller**: Must be accessible via the python -m command. [cite: 22]
* [cite_start]**Tkinter**: Required for the graphical interface. [cite: 1]

---

## How to Use

1. [cite_start]**Placement**: Run py_builder.pyw from the folder containing the Python scripts you wish to compile. [cite: 1, 14]
2. [cite_start]**Selection**: Select the target script from the Detected Scripts listbox. [cite: 11, 19]
3. [cite_start]**Configuration**: Use the checkboxes to toggle Auto-Clean or Dark Mode preferences. [cite: 12, 18]
4. [cite_start]**Build**: Click the BUILD EXE button to start the process. [cite: 13, 20]
    * [cite_start]The tool checks for and installs missing dependencies. [cite: 21, 22]
    * [cite_start]It executes the PyInstaller command with the --onefile flag. [cite: 22]
5. [cite_start]**Output**: On success, the standalone executable is moved from the dist folder to your main directory. [cite: 24, 25]

---

## Technical Details

* [cite_start]**Base Directory**: The tool detects its location whether running as a script or a frozen EXE. [cite: 1]
* [cite_start]**Threading**: Build tasks and folder watching run on separate threads to keep the UI responsive. [cite: 10, 19]
* [cite_start]**Permissions**: Uses a helper function to modify file permissions during directory cleanup. [cite: 3, 4]

---

*Project generated for Py Builder*
