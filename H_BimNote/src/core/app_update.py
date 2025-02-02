import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import subprocess

APP_VERSION = "1.0.0"  # Your app's current version
# UPDATE_URL = "https://github.com/hnanmal/mQ/blob/master/H_BimNote/resource/version.json"  # Replace with your real URL
UPDATE_URL = "https://raw.githubusercontent.com/hnanmal/mQ/refs/heads/master/H_BimNote/resource/version.json"  # Replace with your real URL
# UPDATE_URL = "https://yourwebsite.com/version.json"  # Replace with your real URL


def check_for_update():
    try:
        response = requests.get(UPDATE_URL)
        latest_version_data = response.json()
        latest_version = latest_version_data["version"]
        download_url = latest_version_data["download_url"]

        if latest_version > APP_VERSION:
            answer = messagebox.askyesno(
                "Update Available",
                f"A new version ({latest_version}) is available. Do you want to update now?",
            )
            if answer:
                download_update(download_url)
        else:
            messagebox.showinfo("No Update", "You are using the latest version.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to check for updates: {e}")


def download_update(download_url):
    """Download and replace the old executable."""
    try:
        update_filename = "app_update.exe"  # Temporary filename
        response = requests.get(download_url, stream=True)
        with open(update_filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        messagebox.showinfo(
            "Update Downloaded",
            "The update has been downloaded. The application will restart.",
        )

        # Restart the app with the new update
        apply_update(update_filename)

    except Exception as e:
        messagebox.showerror("Update Failed", f"Failed to download update: {e}")


def apply_update(update_filename):
    """Replace the old exe with the new one and restart."""
    current_exe = sys.executable  # Get current executable path

    # Rename the old exe (backup)
    backup_exe = current_exe + ".old"
    os.rename(current_exe, backup_exe)

    # Move the new update to replace the old executable
    os.rename(update_filename, current_exe)

    # Restart the application
    subprocess.Popen([current_exe])
    sys.exit()


# # Create the UI
# root = tk.Tk()
# root.title("App with Auto-Update")

# update_button = tk.Button(root, text="Check for Updates", command=check_for_update)
# update_button.pack(pady=20)

# root.mainloop()
