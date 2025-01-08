import tkinter as tk

# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from tkinterdnd2 import TkinterDnD

# from tkinter.ttk import Progressbar

from PIL import ImageTk, Image

# import time

# from src.controllers.db_update_manager import DBUpdateManager
from src.core.file_utils import load_from_json
from src.views.upper_tab import (
    create_project_apply_tab,
    create_project_standard_tab,
    create_recentBnotes_tab,
    create_team_standard_tab,
)
from src.views.app_ui_setup import initialize_app


def main():
    # root = tk.Tk()
    # root = ttk.Window(themename="journal")
    root = TkinterDnD.Tk()

    # Apply ttkbootstrap theme
    style = ttk.Style()
    style.theme_use("journal")  # Use your preferred ttkbootstrap theme
    ################

    notebook, state = initialize_app(root)
    root.iconify()
    # root.withdraw()  # Hide the main window while splash is shown
    state.root = root

    splash = show_splash_screen()
    splash.wait_window()  # Wait for the splash screen to close

    # Create parent tabs within the notebook
    create_recentBnotes_tab(state, notebook)

    create_team_standard_tab(state, notebook)

    create_project_standard_tab(state, notebook)

    create_project_apply_tab(state, notebook)

    ## 팀스탠다드 자동 임포트
    # load_from_json(state, "resource/PlantArch_BIM Standard.bnote")

    root.deiconify()
    root.state("zoomed")

    ## 어플리케이션 시작시 메시지
    state.log_widget.write("어서오세요!\n")

    notebook.select(0)

    # # Handle window close event
    # root.protocol("WM_DELETE_WINDOW", lambda: close_app(root, state))

    root.mainloop()


def close_app(root, state):
    """Ensure CEF and other resources are properly shut down."""
    if hasattr(state, "browser_widget"):
        state.browser_widget.on_close()  # Shutdown CEF properly
    root.destroy()


def show_splash_screen():
    """Create and display a splash screen."""
    splash_width = 700
    splash_height = 350

    splash = tk.Toplevel()
    splash.configure(bg="#ebebeb", highlightthickness=5)
    splash.title("B-Note")
    splash.geometry(f"{splash_width}x{splash_height}")
    splash.overrideredirect(True)  # Remove window decorations (close, minimize, etc.)
    splash.wm_attributes("-alpha", 0.9)  # Set transparency

    # Add branding or loading information
    logo_img_ = Image.open("resource/app_logo.png")
    logo_img_ = logo_img_.resize((300, 300), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo_img_)

    tk.Label.image = logo_img

    logo_area = tk.Frame(splash)
    logo_area.pack(side="left")

    text_area = tk.Frame(splash)
    text_area.configure(bg="#ebebeb")
    text_area.pack(padx=20, side="left")

    logo_label = tk.Label(logo_area, image=logo_img)
    logo_label.configure(bg="#ebebeb")
    logo_label.pack()

    text_labe1 = tk.Label(text_area, text="B-Note", font=("Tw Cen MT", 60, "bold"))
    text_labe1.configure(bg="#ebebeb")
    text_labe1.pack(padx=20, pady=20, anchor="nw")

    text_label2 = tk.Label(
        text_area,
        # text="HEC BIM Note, now Loading...",
        text="시작하는중...",
        font=("Arial", 12),
    )
    text_label2.configure(bg="#ebebeb")
    text_label2.pack(padx=20, pady=10, anchor="ne")

    # Center the splash screen
    splash.update_idletasks()
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()

    x = (screen_width // 2) - (splash_width // 2)
    y = (screen_height // 2) - (splash_height // 2)
    splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

    # Close splash screen after 3 seconds
    splash.after(3000, splash.destroy)

    return splash


if __name__ == "__main__":
    main()
