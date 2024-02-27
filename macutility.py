#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys

def check_tkinter_version():
    # Ensure that the tkinter version is compatible with Python 3.11
    try:
        major, minor = tk.Tcl().eval('info patchlevel').split('.')[:2]
        if int(major) < 8 or (int(major) == 8 and int(minor) < 6):
            messagebox.showerror("Error", "Python-tk@3.11 is not installed. Please install the correct version.")
            sys.exit(1)  # Exit if incompatible tkinter version is found
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while checking tkinter version: {e}")
        sys.exit(1)

# Call the function to check tkinter version
check_tkinter_version()

root = tk.Tk()
root.title("macOS Utility Installer")
root.geometry("422x600")

def check_homebrew():
    try:
        subprocess.run(["brew", "--version"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_homebrew():
    if not check_homebrew():
        subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True)
        messagebox.showinfo("Installation", "Homebrew has been installed.")

# Ensure Homebrew is installed
install_homebrew()

def is_app_installed(app):
    try:
        installed_formulas = subprocess.check_output(["brew", "list", "--formula"], text=True).strip().split('\n')
        installed_casks = subprocess.check_output(["brew", "list", "--cask"], text=True).strip().split('\n')
        return app in installed_formulas or app in installed_casks
    except subprocess.CalledProcessError:
        return False

def reset_checkboxes():
    for var in apps.values():
        var.set(False)

def install_apps():
    installation_initiated = False
    for app, var in apps.items():
        if var.get():
            if is_app_installed(app):
                messagebox.showinfo("Already Installed", f"{app} is already installed.")
            else:
                subprocess.Popen(["brew", "install", app], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                installation_initiated = True
    if installation_initiated:
        messagebox.showinfo("Installation", "Installation process initiated.")
    reset_checkboxes()

def select_all_apps():
    for var in apps.values():
        var.set(True)

def unselect_all_apps():
    for var in apps.values():
        var.set(False)

def uninstall_selected_apps():
    for app, var in apps.items():
        if var.get():
            subprocess.Popen(["brew", "uninstall", app], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    messagebox.showinfo("Uninstallation", "Selected applications have been uninstalled.")
    reset_checkboxes()

# Categorized apps setup
categories = {
    "Productivity": ["hammerspoon", "iterm2", "pastebot"],
    "Utilities": ["keycastr", "vanilla", "only-switch", "zoom", "appcleaner"],
    "Creative": ["loom", "bunch", "karabiner-elements"],
    "Browser": ["google-chrome", "Firefox", "brave-browser", "arc", "orion"],
    "Communications": ["chatterino", "discord", "signal", "skype", "slack", "microsoft-teams", "telegram", "thunderbird"]
}

apps = {}

# Scrollable area setup
canvas = tk.Canvas(root, borderwidth=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def _on_frame_configure(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", _on_frame_configure)

# Layout for canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Populate scrollable frame with content
for category, app_list in categories.items():
    frame = ttk.LabelFrame(scrollable_frame, text=category)
    frame.pack(padx=10, pady=5, expand=True, fill="both")
    for app in app_list:
        var = tk.BooleanVar(value=False)
        apps[app] = var
        ttk.Checkbutton(frame, text=app, variable=var).pack(anchor="w")

# Action buttons at the bottom
buttons_frame = ttk.Frame(root)
buttons_frame.pack(fill="x", anchor="s", padx=10, pady=5)

ttk.Button(root, text="Select All Apps", command=select_all_apps).pack(anchor='w', padx=(10, 0), pady=5)
ttk.Button(root, text="Unselect All Apps", command=unselect_all_apps).pack(anchor='w', padx=(10, 0), pady=5)
ttk.Button(root, text="Install Selected Apps", command=install_apps).pack(anchor='w', padx=(10, 0), pady=5)
ttk.Button(root, text="Uninstall Selected Apps", command=uninstall_selected_apps).pack(anchor='w', padx=(10, 0), pady=5)

root.mainloop()
