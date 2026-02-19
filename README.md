# Py Builder

[cite_start]A sleek, **Tkinter-based** GUI utility designed to automate the conversion of Python scripts into standalone executables using **PyInstaller**[cite: 1, 10, 23].

---

## 🚀 Features

* [cite_start]**Automatic Script Detection**: Scans the directory in real-time for `.py` and `.pyw` files[cite: 14, 15].
* [cite_start]**Smart Dependency Management**: Uses AST (Abstract Syntax Trees) to find imports and automatically installs missing modules via `pip`[cite: 6, 21, 22].
* **Adaptive Build Modes**: 
    * [cite_start]**Console Mode**: Automatically applied to `.py` files[cite: 22].
    * [cite_start]**Windowed Mode**: Automatically applied to `.pyw` files using the `--noconsole` flag[cite: 22].
* [cite_start]**Theme Support**: Toggle between **Dark** and **Light** modes with persistent settings[cite: 8, 9, 12, 18].
* [cite_start]**Workspace Cleanup**: Automatically removes `build/`, `dist/`, and `.spec` files after the build to keep your folders clean[cite: 4, 5, 27].
* [cite_start]**Real-Time Logging**: View the full PyInstaller output directly within the application log[cite: 14, 23].

---

## 🛠️ Requirements

* **Python 3.x**
* **PyInstaller** (`pip install pyinstaller`)
* **Tkinter** (usually included with standard Python installations)

---

## 📖 How to Use

1.  [cite_start]**Placement**: Place `py_builder.pyw` in the folder containing the Python scripts you wish to compile[cite: 1].
2.  [cite_start]**Selection**: Launch the app and select your target script from the **Detected Scripts** list[cite: 11, 19].
3.  [cite_start]**Configuration**: Toggle **Auto-Clean** or **Dark Mode** based on your preference[cite: 12].
4.  [cite_start]**Build**: Click **BUILD EXE**[cite: 13].
    * [cite_start]The tool will install any missing dependencies[cite: 22].
    * [cite_start]It will run the PyInstaller command: `pyinstaller --onefile [mode] [script]`[cite: 22].
5.  [cite_start]**Output**: Once finished, your standalone executable will be moved from the `dist` folder directly into your main directory for easy access[cite: 24, 25].

---

## ⚙️ Technical Details

* [cite_start]**Base Directory**: The tool dynamically detects its location, whether running as a script or a frozen executable[cite: 1].
* [cite_start]**Threading**: Builds are processed in a background thread to prevent the GUI from freezing[cite: 10, 19].
* [cite_start]**Permissions**: Includes a helper to handle read-only file errors during cleanup[cite: 3, 4].

---

*Generated for Py Builder Project*
