#!/usr/bin/env python3
# Corrected tkinter import
import tkinter as tk
root = tk.Tk()
root.geometry("422x700")
from tkinter import ttk
from tkinter import messagebox
import subprocess

def check_homebrew():
    try:
        subprocess.run(["brew", "--version"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_homebrew():
    subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True)
    messagebox.showinfo("Installation", "Homebrew has been installed.")

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
    installation_initiated = False  # Flag to track if any installations were actually initiated
    for app, var in apps.items():
        if var.get():  # Check if the app is selected for installation
            if is_app_installed(app):
                messagebox.showinfo("Already Installed", f"{app} is already installed.")
            else:
                subprocess.Popen(["brew", "install", app], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                installation_initiated = True  # Set the flag to True as an installation was initiated
    if installation_initiated:
        messagebox.showinfo("Installation", "Installation process initiated.")
    reset_checkboxes()

root.title("macOS Utility Installer")

if not check_homebrew():
    if messagebox.askyesno("Homebrew Not Found", "Homebrew is not installed. Would you like to install it?"):
        install_homebrew()

# Categorized apps setup
categories = {
    "Productivity": ["hammerspoon", "iterm2"],
    "Utilities": ["keycastr", "vanilla", "only-switch"],
    "Creative": ["loom", "bunch"],
    "Browser": ["google-chrome", "brave-browser", "arc"],
    "Communications": ["chatterino", "discord", "signal", "skype", "slack", "microsoft-teams", "telegram", "thunderbird"]  # Added Communications category
}

# Adjust apps dictionary to be empty initially
apps = {}

# Create LabelFrames and Checkbuttons for each category
for category_name, apps_list in categories.items():
    category_frame = ttk.LabelFrame(root, text=category_name)
    category_frame.pack(padx=10, pady=5, fill="both", expand=True)
    for app_name in apps_list:
        apps[app_name] = tk.BooleanVar(value=False)
        ttk.Checkbutton(category_frame, text=app_name, variable=apps[app_name]).pack(anchor='w', side="top", padx=5, pady=2)


def select_all_apps():
    for var in apps.values():
        var.set(True)

def uninstall_selected_apps():
    for app, var in apps.items():
        if var.get():
            subprocess.Popen(["brew", "uninstall", app], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    messagebox.showinfo("Uninstallation", "Selected applications have been uninstalled.")
    reset_checkboxes()

# Create a frame to contain the select and unselect buttons
button_frame = tk.Frame(root)
button_frame.pack(padx=5, pady=5)

# Define the unselect_all_apps function
def unselect_all_apps():
    for var in apps.values():
        var.set(False)

ttk.Button(button_frame, text="Select All Apps", command=select_all_apps).pack(side='left', padx=5, pady=5)
ttk.Button(button_frame, text="Unselect All Apps", command=unselect_all_apps).pack(side='left', padx=5, pady=5)

# Adjust other buttons similarly
ttk.Button(root, text="Install Selected Apps", command=install_apps).pack(padx=5, pady=5)
ttk.Button(root, text="Uninstall Selected Apps", command=uninstall_selected_apps).pack(padx=5, pady=5)

root.mainloop()
