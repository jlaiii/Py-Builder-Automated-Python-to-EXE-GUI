import os
import sys
import subprocess
import shutil
import time
import ast
import stat
import json
import threading
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ===============================
# CONFIG & SETTINGS
# ===============================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_FILE = os.path.join(BASE_DIR, "builder_settings.json")

class Settings:
    def __init__(self):
        self.auto_clean = True
        self.dark_mode = True
        self.load()

    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    self.auto_clean = data.get("auto_clean", True)
                    self.dark_mode = data.get("dark_mode", True)
            except Exception:
                pass

    def save(self):
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.__dict__, f, indent=4)
        except Exception:
            pass

prefs = Settings()

# ===============================
# UTILS
# ===============================
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clean_folders():
    targets = [os.path.join(BASE_DIR, "build"), os.path.join(BASE_DIR, "dist")]
    time.sleep(2)
    for target in targets:
        if os.path.exists(target):
            try:
                shutil.rmtree(target, onerror=remove_readonly)
            except Exception:
                pass
    
    for f in os.listdir(BASE_DIR):
        if f.endswith(".spec"):
            try:
                os.remove(os.path.join(BASE_DIR, f))
            except Exception:
                pass

def find_imports(file_path):
    modules = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    modules.add(n.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    modules.add(node.module.split(".")[0])
    except Exception:
        pass
    return modules

# ===============================
# GUI APPLICATION
# ===============================
class PyBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Py Builder")
        self.root.geometry("800x700")
        
        self.themes = {
            "dark": {
                "bg": "#1e1e1e", "panel": "#252526", "fg": "#d4d4d4", 
                "btn": "#007acc", "btn_fg": "white", "border": "#3e3e42", "log_bg": "#000000"
            },
            "light": {
                "bg": "#f3f3f3", "panel": "#ffffff", 
                "fg": "#333333", 
                "btn": "#007acc", "btn_fg": "white", "border": "#cccccc", "log_bg": "#ffffff"
            }
        }
        
        self.current_theme = "dark" if prefs.dark_mode else "light"
        self.last_file_state = []
        
        self.setup_ui()
        self.apply_theme()
        
        # Start Watcher and Initial Dependency Check
        threading.Thread(target=self.folder_watcher, daemon=True).start()
        # Silent check for PyInstaller
        threading.Thread(target=self.bootstrap_dependencies, daemon=True).start()

    def setup_ui(self):
        self.header = tk.Frame(self.root, height=50, bd=0)
        self.header.pack(fill="x")
        self.title_label = tk.Label(self.header, text="PY BUILDER", font=("Segoe UI", 14, "bold"))
        self.title_label.pack(pady=10)

        self.container = tk.Frame(self.root, padx=20, pady=20)
        self.container.pack(fill="both", expand=True)

        top_frame = tk.Frame(self.container)
        top_frame.pack(fill="x", side="top")

        self.list_frame = tk.LabelFrame(top_frame, text="Detected Scripts (Auto-Refresh)", padx=5, pady=5, font=("Segoe UI", 9))
        self.list_frame.pack(side="left", fill="both", expand=True)
        
        self.file_listbox = tk.Listbox(self.list_frame, height=10, font=("Segoe UI", 10), borderwidth=0, highlightthickness=1)
        self.file_listbox.pack(fill="both", expand=True)
        
        self.ctrl_frame = tk.LabelFrame(top_frame, text="Settings", padx=10, pady=5, font=("Segoe UI", 9))
        self.ctrl_frame.pack(side="right", fill="y", padx=(10, 0))

        self.clean_var = tk.BooleanVar(value=prefs.auto_clean)
        self.clean_check = tk.Checkbutton(self.ctrl_frame, text="Auto-Clean", variable=self.clean_var, command=self.toggle_clean)
        self.clean_check.pack(anchor="w", pady=5)

        self.theme_var = tk.BooleanVar(value=prefs.dark_mode)
        self.theme_check = tk.Checkbutton(self.ctrl_frame, text="Dark Mode", variable=self.theme_var, command=self.toggle_theme)
        self.theme_check.pack(anchor="w", pady=5)
        
        self.build_btn = tk.Button(self.ctrl_frame, text="BUILD EXE", font=("Segoe UI", 10, "bold"),
                                   command=self.initiate_build, width=15, borderwidth=0)
        self.build_btn.pack(fill="x", pady=20)

        self.log_label = tk.Label(self.container, text="Build Log", font=("Segoe UI", 9))
        self.log_label.pack(anchor="w", pady=(15, 0))
        
        self.log_area = scrolledtext.ScrolledText(self.container, height=20, font=("Consolas", 10), borderwidth=0, highlightthickness=1)
        self.log_area.pack(fill="both", expand=True)

    def bootstrap_dependencies(self):
        """Silently checks if PyInstaller is ready by trying to import it."""
        try:
            # Try to actually import it; this is more reliable than find_spec
            import PyInstaller
        except ImportError:
            # Only if import fails do we log and install
            self.log("[SYSTEM] PyInstaller not found. Auto-installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.log("[SYSTEM] PyInstaller installed successfully.")
            except Exception:
                self.log("[ERROR] Auto-install failed. Please run 'pip install pyinstaller' manually.")

    def folder_watcher(self):
        while True:
            try:
                files = sorted([f for f in os.listdir(BASE_DIR) if f.endswith(".py") or f.endswith(".pyw")])
                if files != self.last_file_state:
                    self.last_file_state = files
                    self.file_listbox.delete(0, tk.END)
                    for f in files:
                        self.file_listbox.insert(tk.END, f)
            except Exception:
                pass
            time.sleep(1)

    def apply_theme(self):
        t = self.themes[self.current_theme]
        self.root.configure(bg=t["bg"])
        self.header.configure(bg=t["panel"])
        self.title_label.configure(bg=t["panel"], fg=t["btn"])
        self.container.configure(bg=t["bg"])
        self.list_frame.configure(bg=t["bg"], fg=t["fg"])
        self.file_listbox.configure(bg=t["panel"], fg=t["fg"], highlightbackground=t["border"], selectbackground=t["btn"])
        self.ctrl_frame.configure(bg=t["bg"], fg=t["fg"])
        self.clean_check.configure(bg=t["bg"], fg=t["fg"], selectcolor=t["panel"], activebackground=t["bg"], activeforeground=t["fg"])
        self.theme_check.configure(bg=t["bg"], fg=t["fg"], selectcolor=t["panel"], activebackground=t["bg"], activeforeground=t["fg"])
        self.build_btn.configure(bg=t["btn"], fg=t["btn_fg"])
        self.log_label.configure(bg=t["bg"], fg=t["fg"])
        self.log_area.configure(bg=t["log_bg"], fg=t["fg"], highlightbackground=t["border"])

    def toggle_theme(self):
        self.current_theme = "dark" if self.theme_var.get() else "light"
        prefs.dark_mode = self.theme_var.get()
        prefs.save()
        self.apply_theme()

    def toggle_clean(self):
        prefs.auto_clean = self.clean_var.get()
        prefs.save()

    def log(self, text):
        self.log_area.insert(tk.END, f"{text}\n")
        self.log_area.see(tk.END)

    def initiate_build(self):
        idx = self.file_listbox.curselection()
        if not idx:
            messagebox.showwarning("Selection Required", "Please select a script.")
            return
        
        script_name = self.file_listbox.get(idx[0])
        self.build_btn.config(state="disabled", text="BUILDING...")
        self.log_area.delete("1.0", tk.END)
        threading.Thread(target=self.process_task, args=(script_name,), daemon=True).start()

    def process_task(self, script_name):
        script_path = os.path.join(BASE_DIR, script_name)
        start_time = time.time()
   
        si = None
        if os.name == 'nt':
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0 

        self.log(f"--- STARTING BUILD: {script_name} ---")
        
        imports = find_imports(script_path)
        builtin = {"sys", "os", "time", "json", "math", "random", "subprocess", "shutil", "tkinter", "argparse", "ast", "stat"}
        for mod in imports:
            if mod in builtin: continue
            try:
                importlib.import_module(mod)
            except ImportError:
                self.log(f"Installing missing dependency: {mod}")
                subprocess.run([sys.executable, "-m", "pip", "install", mod], 
                               capture_output=True, startupinfo=si)

        mode = "--noconsole" if script_name.endswith(".pyw") else "--console"
        command = [sys.executable, "-m", "PyInstaller", "--onefile", mode, script_name]
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, cwd=BASE_DIR, startupinfo=si)

        for line in process.stdout:
            self.log(line.strip())

        process.wait()
        end_time = time.time()

        extension = ".exe" if os.name == 'nt' else ""
        exe_filename = os.path.splitext(script_name)[0] + extension
        source_path = os.path.join(BASE_DIR, "dist", exe_filename)
        destination_path = os.path.join(BASE_DIR, exe_filename)

        success = False
        if os.path.exists(source_path):
            try:
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                shutil.move(source_path, destination_path)
                success = True
            except Exception as e:
                self.log(f"FILE ERROR: {str(e)}")

        self.log("\n" + "="*50)
        self.log("FINAL BUILD SUMMARY")
        self.log("="*50)
        self.log(f"Result:        {'SUCCESS' if success else 'FAILED'}")
        self.log(f"Build Time:    {end_time - start_time:.2f}s")
        if success: self.log(f"Output Path:   {destination_path}")
        self.log("="*50)

        if prefs.auto_clean:
            self.log("\nCleaning temporary files...")
            clean_folders()

        self.build_btn.config(state="normal", text="BUILD EXE")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyBuilderGUI(root)
    root.mainloop()