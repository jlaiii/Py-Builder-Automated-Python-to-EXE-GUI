# 🏗️ Py Builder — Automated Python to EXE GUI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/Engine-PyInstaller-orange?style=flat" alt="PyInstaller">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="MIT">
</p>

**Py Builder** is a lightweight desktop GUI that turns your Python scripts into standalone `.exe` files with a single click. Built on top of PyInstaller, it handles everything — dependency scanning, auto-install, build configuration, and cleanup — so you don't have to touch the command line.

---

## ✨ Features

- **One-Click EXE Builds** — select any `.py` or `.pyw` file and build it into a single-file executable
- **Smart Dependency Check** — scans your script's AST for imports and auto-installs missing packages via pip
- **Console Auto-Detection** — `.pyw` files get `--noconsole`, `.py` files get `--console` — handled automatically
- **Dual Log Views** — **Build Log** shows clean PyInstaller output with a build summary (time, size, result); **All Log** captures everything: startup diagnostics, dependency checks, warnings, errors
- **Auto-Clean** — optionally removes `build/`, `dist/`, and `.spec` files after each successful build
- **Folder Watcher** — drop a new script into the folder and it instantly appears in the list
- **Persistent Settings** — dark/light theme and auto-clean preferences saved between sessions

---

## 🚀 Quick Start

### Requirements

- **Windows 10/11**
- **Python 3.10+** — [Download](https://python.org/downloads)

### Install & Run

```bash
git clone https://github.com/jlaiii/Py-Builder-Automated-Python-to-EXE-GUI.git
cd Py-Builder-Automated-Python-to-EXE-GUI
python py_builder.pyw
```

> **No setup needed.** Py Builder auto-installs PyInstaller on first launch. Place it in any project folder with your scripts and double-click.

---

## 📖 Usage

1. **Place** `py_builder.pyw` in your project folder alongside your Python scripts
2. **Launch** the app — it auto-detects all `.py` / `.pyw` files in the folder
3. **Select** a script from the list
4. **Click** `BUILD EXE` and watch the progress
5. Your `.exe` appears in the same folder when done

---

## ⚙️ Settings

| Setting           | Description |
|-------------------|-------------|
| **Auto-Clean**    | Removes `build/`, `dist/`, and `.spec` files after each build |
| **Dark Mode**     | Toggle between dark and light UI themes |

---

## 🔧 Tech Stack

```
Tkinter        → Native GUI (no extra dependencies for the UI)
PyInstaller    → Backend EXE compiler
AST            → Static import detection from source code
subprocess     → Isolated build commands with hidden console
threading      → Responsive UI during builds and folder watching
```

---

## 📁 Project Structure

```
├── py_builder.pyw           # Main application (double-click to run)
├── requirements.txt         # Only PyInstaller (auto-installed)
├── builder_settings.json    # Auto-generated user preferences
├── docs/
│   └── index.html           # GitHub Pages website
└── README.md
```

---

## 🤝 Contributing

Found a bug or have a feature idea? Open an [issue](https://github.com/jlaiii/Py-Builder-Automated-Python-to-EXE-GUI/issues) or submit a pull request.

---

<div align="center">
  <sub>Made with ❤️ by <a href="https://github.com/jlaiii">jlaiii</a></sub>
</div>
