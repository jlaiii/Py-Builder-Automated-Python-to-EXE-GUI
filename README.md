# Py Builder — Automated Python to EXE GUI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/Engine-PyInstaller-orange?style=flat" alt="PyInstaller">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="MIT">
</p>

**Py Builder** is a lightweight desktop GUI that turns your Python scripts into standalone `.exe` files with a single click. Built on PyInstaller, it handles everything — dependency scanning, auto-install, build configuration, and cleanup — so you never need to open a terminal.

---

## Features

- **One-Click EXE Builds** — select any `.py` or `.pyw` file and build it into a single-file executable
- **AST Import Scanner** — parses your script at the syntax-tree level to detect imports and auto-installs missing pip packages
- **Console Auto-Detection** — `.pyw` scripts get `--noconsole`, `.py` scripts keep the terminal window — handled automatically
- **Dual Log Views** — **Build Log** for clean PyInstaller output with a final summary; **All Log** for startup diagnostics, dependency checks, and every warning
- **Auto-Clean** — optionally removes `build/`, `dist/`, and `.spec` files after each successful build
- **Live Folder Watcher** — drop a new script in the folder and it instantly appears in the list
- **Dark & Light Themes** — native-feeling UI with persistent preferences
- **Zero-Setup Launch** — auto-installs PyInstaller on first run, no manual `pip install` needed

---

## Quick Start

### Requirements

- **Windows 10/11**
- **Python 3.10+** — [Download](https://python.org/downloads)

### Install & Run

```bash
git clone https://github.com/jlaiii/Py-Builder-Automated-Python-to-EXE-GUI.git
cd Py-Builder-Automated-Python-to-EXE-GUI
python py_builder.pyw
```

No setup needed. Py Builder auto-installs PyInstaller on first launch. Place `py_builder.pyw` in any project folder alongside your scripts and double-click.

---

## Usage

1. Place `py_builder.pyw` in your project folder with your Python scripts
2. Launch the app — it auto-detects all `.py` / `.pyw` files in the folder
3. Select a script from the list
4. Click `BUILD EXE` and watch the progress in the log tabs
5. Your `.exe` appears in the same folder

---

## Settings

| Setting | Description |
|---|---|
| **Auto-Clean** | Removes `build/`, `dist/`, and `.spec` files after each build |
| **Dark Mode** | Toggle between dark and light UI themes |

---

## Tech Stack

```
Tkinter        → Native GUI (no extra dependencies for the UI)
PyInstaller    → Backend EXE compiler
AST            → Static import detection from Python source code
subprocess     → Isolated build commands with hidden console
threading      → Responsive UI during builds and folder watching
```

---

## Project Structure

```
Py-Builder-Automated-Python-to-EXE-GUI/
|   py_builder.pyw           # Main application
|   requirements.txt         # PyInstaller dependency
|   builder_settings.json    # Auto-generated preferences
|-- docs/
|   |   index.html           # GitHub Pages website
|   |-- .nojekyll
```

---

## Contributing

Found a bug or have a feature idea? Open an [issue](https://github.com/jlaiii/Py-Builder-Automated-Python-to-EXE-GUI/issues) or submit a pull request.

---

<div align="center">
  <sub>Built by <a href="https://github.com/jlaiii">jlaiii</a> &middot; <a href="https://jlaiii.github.io/Py-Builder-Automated-Python-to-EXE-GUI/">Website</a></sub>
</div>
