# Py Builder

Py Builder is a lightweight, automated GUI tool designed to convert Python scripts (.py and .pyw) into standalone executable files (.exe). It simplifies the PyInstaller process by automatically detecting dependencies, managing build settings, and cleaning up temporary build artifacts.

## Features

* **Automatic Dependency Management**: Scans your script for required libraries and installs them via pip if they are missing from the system.
* **One-Click Builds**: Select a script from the auto-refreshing list and build it into a single-file executable.
* **Console Detection**: Automatically configures the build for windowed mode (noconsole) if the source file is a .pyw file.
* **Live Folder Watching**: The UI automatically updates when you add or remove Python files in the project directory.
* **Built-in Clean Up**: Automatically removes 'build' folders and '.spec' files after a successful compilation to keep your directory clean.
* **Interface Customization**: Supports both Dark and Light modes with persistent settings.
* **Real-time Logging**: View the full PyInstaller output directly within the application window.

## Installation

### Prerequisites

* Python 3.x installed on your system.
* Windows (recommended for .exe generation).

### Setup

1.  Download the `py_builder.pyw` file.
2.  Place the file in the directory where your Python projects are located.
3.  Double-click `py_builder.pyw` to run.

Note: On the first run, the application will automatically install PyInstaller if it is not already present in your Python environment.

## Usage

1.  **Select a Script**: All .py and .pyw files in the current folder will appear in the "Detected Scripts" list.
2.  **Configure Settings**: 
    * Enable **Auto-Clean** to remove temporary files after the build.
    * Toggle **Dark Mode** for your visual preference.
3.  **Build**: Click the **BUILD EXE** button. 
4.  **Result**: Once the process finishes, your executable will be located in the same folder as the original script.

## Technical Details

The application uses a bootstrap threading system to ensure that the GUI remains responsive while checking for system dependencies. It utilizes the following standard and third-party components:

* **Tkinter**: For the graphical user interface.
* **PyInstaller**: The backend engine for executable generation.
* **AST (Abstract Syntax Trees)**: To intelligently parse scripts and identify required imports.
* **Subprocess**: To manage pip installations and build commands in isolated threads.

## License

This project is open-source and available for modification and distribution.
