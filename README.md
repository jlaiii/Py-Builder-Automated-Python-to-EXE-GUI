# Py Builder

A Tkinter-based GUI utility designed to automate the conversion of Python scripts into standalone executables using PyInstaller.

---

## Features

* **Automatic Script Detection**: Scans the directory in real-time for .py and .pyw files.
* **Smart Dependency Management**: Uses Abstract Syntax Trees to find imports and attempts to install missing modules via pip.
* **Adaptive Build Modes**: 
    * **Console Mode**: Automatically applied to .py files.
    * **Windowed Mode**: Automatically applied to .pyw files using the --noconsole flag.
* **Theme Support**: Includes Dark and Light modes with settings that persist in a JSON file.
* **Workspace Cleanup**: Optionally removes build, dist, and .spec files after the build process is complete.
* **Real-Time Logging**: Displays the full PyInstaller output directly within the application scrolled text area.

---

## Requirements

* **Python 3.x**
* **PyInstaller**: Must be installed and accessible via the python -m command.
* **Tkinter**: Required for the graphical interface (usually included with Python).

---

## How to Use

1. **Placement**: Run py_builder.pyw from the same folder containing the Python scripts you wish to compile.
2. **Selection**: Select the target script from the Detected Scripts listbox.
3. **Configuration**: Use the checkboxes to toggle Auto-Clean or Dark Mode preferences.
4. **Build**: Click the BUILD EXE button to start the process.
    * The tool checks for and installs missing dependencies.
    * It executes the PyInstaller command with the --onefile flag.
5. **Output**: On success, the standalone executable is moved from the temporary dist folder to your main directory.

---

## Technical Details

* **Base Directory**: The tool detects its location whether running as a script or a frozen EXE.
* **Threading**: Build tasks and folder watching run on separate threads to keep the UI responsive.
* **Permissions**: Uses a helper function to modify file permissions to ensure successful directory cleanup.

---

*Project generated for Py Builder*
