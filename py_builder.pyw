import sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRASH_LOG_PATH = os.path.join(BASE_DIR, "crash_log.txt")

_CRASH_FH = open(CRASH_LOG_PATH, "w", encoding="utf-8")
sys.stderr = _CRASH_FH

import datetime

def _crash(msg):
    try:
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        _CRASH_FH.write(f"[{ts}] {msg}\n")
        _CRASH_FH.flush()
    except:
        pass

_crash("Boot: crash log active")

if sys.platform == "win32" and not sys.executable.lower().endswith("pythonw.exe"):
    idx = sys.executable.lower().rfind("python.exe")
    _pythonw = sys.executable[:idx] + "pythonw.exe" if idx != -1 else ""
    if _pythonw and os.path.isfile(_pythonw):
        _crash(f"Re-launching via pythonw: {_pythonw}")
        import subprocess as _sp
        _sp.Popen(
            [_pythonw, __file__],
            creationflags=_sp.DETACHED_PROCESS | _sp.CREATE_NO_WINDOW,
            close_fds=True
        )
        sys.exit()
    else:
        _crash("pythonw not found, freeing console")
        try:
            import ctypes as _ct
            _ct.windll.kernel32.FreeConsole()
        except:
            pass

try:
    import ctypes as _ct2
    _ct2.windll.user32.ShowWindow(_ct2.windll.kernel32.GetConsoleWindow(), 0)
except:
    pass

# ===============================
# DEPENDENCY AUTO-CHECK & INSTALL
# ===============================
REQUIRED = {"pyinstaller": "PyInstaller"}

_boot_log = []

def _boot(level, msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    _boot_log.append((ts, level, msg))
    _crash(f"[{level}] {msg}")

def _ensure_packages():
    _boot("INFO", "Scanning dependencies...")
    missing = []
    for disp, pkg in REQUIRED.items():
        try:
            __import__(pkg)
            ver = getattr(sys.modules.get(pkg), "__version__", "?")
            _boot("OK", f"{disp} v{ver} ready")
        except ImportError:
            _boot("WARN", f"{disp} MISSING")
            missing.append(disp)

    if not missing:
        _boot("OK", "All dependencies ready")
        return True

    _boot("INFO", f"Installing: {', '.join(missing)}")
    try:
        import subprocess
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check"] + missing,
            capture_output=True, text=True, creationflags=flags
        )
        if r.returncode == 0:
            _boot("OK", "Installation complete")
            for pkg in missing:
                try:
                    __import__(pkg)
                    _boot("OK", f"{pkg} verified OK")
                except ImportError:
                    _boot("ERROR", f"{pkg} verification FAILED")
            return True
        else:
            err = r.stderr.strip() or "Unknown pip error"
            _boot("ERROR", f"pip failed: {err}")
            return False
    except Exception as e:
        _boot("ERROR", f"Install error: {e}")
        return False

_ensure_packages()

_boot("INFO", f"PyBuilder Start — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
_boot("INFO", f"OS: {sys.platform}")
_boot("INFO", f"Python: {sys.version.split()[0]}")
_boot("INFO", f"Work Dir: {BASE_DIR}")

import subprocess
import shutil
import time
import ast
import stat
import json
import threading
import importlib.util
import importlib
import queue
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

_boot("INFO", "All stdlib modules loaded OK")

# ===============================
# CONFIG & SETTINGS
# ===============================
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
                json.dump({"auto_clean": self.auto_clean, "dark_mode": self.dark_mode}, f, indent=4)
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
        self.root.geometry("850x720")

        self.all_log_queue = queue.Queue()
        self.build_log_queue = queue.Queue()

        self.themes = {
            "dark": {
                "bg": "#1e1e1e", "panel": "#252526", "fg": "#d4d4d4",
                "btn": "#007acc", "btn_fg": "white", "border": "#3e3e42",
                "log_bg": "#0d0d0d", "tab_active": "#007acc", "tab_inactive": "#2d2d2d",
                "select": "#094771"
            },
            "light": {
                "bg": "#f3f3f3", "panel": "#ffffff",
                "fg": "#333333",
                "btn": "#007acc", "btn_fg": "white", "border": "#cccccc",
                "log_bg": "#ffffff", "tab_active": "#007acc", "tab_inactive": "#d0d0d0",
                "select": "#cce5ff"
            }
        }

        self.current_theme = "dark" if prefs.dark_mode else "light"
        self.last_file_state = []

        self.setup_ui()
        self.apply_theme()

        threading.Thread(target=self.folder_watcher, daemon=True).start()
        self.after(100, self._process_log_queues)
        self._flush_startup_logs()

    def _flush_startup_logs(self):
        for ts, level, msg in _boot_log:
            self.all_log(ts, level, msg)
        _boot_log.clear()

    def after(self, ms, func):
        self.root.after(ms, func)

    def _process_log_queues(self):
        try:
            while True:
                target, ts, msg = self.all_log_queue.get_nowait()
                self._write_log(target, ts, msg)
        except queue.Empty:
            pass
        try:
            while True:
                target, ts, msg = self.build_log_queue.get_nowait()
                self._write_log(target, ts, msg)
        except queue.Empty:
            pass
        self.after(100, self._process_log_queues)

    def _write_log(self, widget, ts, msg):
        widget.insert(tk.END, f"[{ts}] {msg}\n")
        widget.see(tk.END)

    def all_log(self, ts, level, msg):
        if hasattr(self, "all_log_area"):
            self.all_log_queue.put((self.all_log_area, ts, f"[{level}] {msg}"))

    def build_log(self, msg):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        if hasattr(self, "build_log_area"):
            self.build_log_queue.put((self.build_log_area, ts, msg))

    def setup_ui(self):
        self.header = tk.Frame(self.root, height=50, bd=0)
        self.header.pack(fill="x")
        self.title_label = tk.Label(self.header, text="PY BUILDER", font=("Segoe UI", 14, "bold"))
        self.title_label.pack(pady=10)

        self.container = tk.Frame(self.root, padx=20, pady=20)
        self.container.pack(fill="both", expand=True)

        top_frame = tk.Frame(self.container)
        top_frame.pack(fill="x", side="top")

        self.list_frame = tk.LabelFrame(top_frame, text="Detected Scripts", padx=5, pady=5, font=("Segoe UI", 9))
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

        self.tab_frame = tk.Frame(self.container)
        self.tab_frame.pack(fill="x", pady=(15, 0))

        self.tab_build = tk.Label(self.tab_frame, text="  Build Log  ", font=("Segoe UI", 10, "bold"),
                                  padx=14, pady=5, cursor="hand2")
        self.tab_build.pack(side="left")
        self.tab_build.bind("<Button-1>", lambda e: self._switch_tab("build"))

        self.tab_all = tk.Label(self.tab_frame, text="  All Log  ", font=("Segoe UI", 10, "bold"),
                                padx=14, pady=5, cursor="hand2")
        self.tab_all.pack(side="left", padx=(2, 0))
        self.tab_all.bind("<Button-1>", lambda e: self._switch_tab("all"))

        self.log_container = tk.Frame(self.container)
        self.log_container.pack(fill="both", expand=True)

        self.build_log_area = scrolledtext.ScrolledText(self.log_container, height=18, font=("Consolas", 10),
                                                         borderwidth=0, highlightthickness=1)
        self.all_log_area = scrolledtext.ScrolledText(self.log_container, height=18, font=("Consolas", 10),
                                                       borderwidth=0, highlightthickness=1)

        self.build_log_area.pack(fill="both", expand=True)
        self._active_tab = "build"

    def _switch_tab(self, tab):
        self._active_tab = tab
        self.all_log_area.pack_forget()
        self.build_log_area.pack_forget()
        if tab == "build":
            self.build_log_area.pack(fill="both", expand=True)
        else:
            self.all_log_area.pack(fill="both", expand=True)
        self.apply_theme()

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
        self.file_listbox.configure(bg=t["panel"], fg=t["fg"], highlightbackground=t["border"],
                                     selectbackground=t["select"], selectforeground=t["fg"])
        self.file_listbox.configure(foreground=t["fg"])
        self.ctrl_frame.configure(bg=t["bg"], fg=t["fg"])
        self.clean_check.configure(bg=t["bg"], fg=t["fg"], selectcolor=t["panel"],
                                    activebackground=t["bg"], activeforeground=t["fg"])
        self.theme_check.configure(bg=t["bg"], fg=t["fg"], selectcolor=t["panel"],
                                    activebackground=t["bg"], activeforeground=t["fg"])
        self.build_btn.configure(bg=t["btn"], fg=t["btn_fg"])
        self.tab_frame.configure(bg=t["bg"])
        self.log_container.configure(bg=t["bg"])

        for area in (self.build_log_area, self.all_log_area):
            area.configure(bg=t["log_bg"], fg=t["fg"], insertbackground=t["fg"],
                           highlightbackground=t["border"])

        active_bg = t["tab_active"]
        inactive_bg = t["tab_inactive"]
        active_fg = "white"
        inactive_fg = t["fg"]
        sel_bg = t["select"]

        self.tab_build.configure(
            bg=active_bg if self._active_tab == "build" else inactive_bg,
            fg=active_fg if self._active_tab == "build" else inactive_fg
        )
        self.tab_all.configure(
            bg=active_bg if self._active_tab == "all" else inactive_bg,
            fg=active_fg if self._active_tab == "all" else inactive_fg
        )

    def toggle_theme(self):
        self.current_theme = "dark" if self.theme_var.get() else "light"
        prefs.dark_mode = self.theme_var.get()
        prefs.save()
        self.apply_theme()

    def toggle_clean(self):
        prefs.auto_clean = self.clean_var.get()
        prefs.save()

    def initiate_build(self):
        idx = self.file_listbox.curselection()
        if not idx:
            messagebox.showwarning("Selection Required", "Please select a script.")
            return

        script_name = self.file_listbox.get(idx[0])
        self.build_btn.config(state="disabled", text="BUILDING...")
        self.build_log_area.delete("1.0", tk.END)
        self.all_log("INFO", f"Build initiated for: {script_name}")
        threading.Thread(target=self.process_task, args=(script_name,), daemon=True).start()

    def process_task(self, script_name):
        script_path = os.path.join(BASE_DIR, script_name)
        start_time = time.time()

        si = None
        if os.name == 'nt':
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0

        self.build_log(f"--- BUILD: {script_name} ---")
        self.all_log("INFO", f"Building: {script_name} | Mode: {'noconsole' if script_name.endswith('.pyw') else 'console'}")

        imports = find_imports(script_path)
        builtin = {"sys", "os", "time", "json", "math", "random", "subprocess", "shutil",
                   "tkinter", "argparse", "ast", "stat", "pathlib", "re", "collections",
                   "itertools", "datetime", "functools", "hashlib", "io", "tempfile",
                   "threading", "queue", "urllib", "http", "socket", "ssl", "email",
                   "xml", "html", "csv", "configparser", "logging", "unittest", "traceback",
                   "difflib", "textwrap", "string", "types", "copy", "pprint", "enum",
                   "dataclasses", "typing", "abc", "base64", "binascii", "struct"}
        for mod in imports:
            if mod in builtin:
                continue
            try:
                importlib.import_module(mod)
            except ImportError:
                self.build_log(f"Installing dependency: {mod}")
                self.all_log("INFO", f"Auto-installing: {mod}")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", mod],
                                   capture_output=True, startupinfo=si)
                    self.all_log("OK", f"{mod} installed")
                except Exception:
                    self.all_log("WARN", f"{mod} install failed — build may still succeed")

        mode = "--noconsole" if script_name.endswith(".pyw") else "--console"
        command = [sys.executable, "-m", "PyInstaller", "--onefile", mode, script_name]

        self.build_log(f"Command: {' '.join(command)}")
        self.all_log("INFO", f"Running PyInstaller...")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, cwd=BASE_DIR, startupinfo=si)

        for line in process.stdout:
            stripped = line.strip()
            self.build_log(stripped)
            if stripped and ("ERROR" in stripped or "WARNING" in stripped or "CRITICAL" in stripped):
                self.all_log("WARN", stripped)

        process.wait()
        end_time = time.time()

        if process.returncode != 0:
            self.all_log("ERROR", f"PyInstaller exited with code {process.returncode}")

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
                self.build_log(f"FILE ERROR: {e}")
                self.all_log("ERROR", f"Move error: {e}")

        summary_lines = [
            "",
            "=" * 50,
            "FINAL BUILD SUMMARY",
            "=" * 50,
            f"Result:      {'SUCCESS' if success else 'FAILED'}",
            f"Build Time:  {end_time - start_time:.2f}s",
        ]
        if success:
            summary_lines.append(f"Output:      {destination_path}")
            summary_lines.append(f"File Size:   {os.path.getsize(destination_path) / 1024:.1f} KB")
        summary_lines.append("=" * 50)

        for line in summary_lines:
            self.build_log(line)

        self.all_log("OK" if success else "ERROR",
                     f"Build {'succeeded' if success else 'FAILED'} in {end_time - start_time:.2f}s")

        if prefs.auto_clean:
            self.build_log("Cleaning temporary files...")
            self.all_log("INFO", "Auto-cleaning build artifacts")
            clean_folders()

        self.build_btn.config(state="normal", text="BUILD EXE")

if __name__ == "__main__":
    try:
        _crash("Boot: entering mainloop")
        root = tk.Tk()
        app = PyBuilderGUI(root)
        root.mainloop()
    except Exception:
        import traceback
        tb = traceback.format_exc()
        _crash(f"FATAL:\n{tb}")
        try:
            _CRASH_FH.close()
        except:
            pass
        try:
            import tkinter.messagebox as _mb
            _mb.showerror("PyBuilder Fatal Error", f"Check crash_log.txt\n\n{tb.splitlines()[-1]}")
        except:
            pass
        sys.exit(1)
    finally:
        try:
            _CRASH_FH.close()
        except:
            pass
