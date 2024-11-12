import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, Menu
import json

from src.core.file_utils import load_from_json, save_to_json_teamStdInfo
from src.models.app_state import AppState
from src.views.logging_utils import setup_logging_frame


def define_styles():
    style = ttk.Style()
    # Define a custom style for the main Notebook
    style.configure(
        "Main.TNotebook",
        tabposition="nw",  # north, tabs at the top
        # background="lightgrey",
        tabmargins=[5, 5, 5, 5],
    )  # space around tabs

    style.configure(
        "Main.TNotebook.Tab",
        background="white",
        foreground="black",
        padding=[70, 0],
        font=("Helvetica", 12, "bold"),
    )

    # Define a custom style for the subtabs
    style.configure(
        "Subtab.TNotebook",
        # background="white",
        tabposition="nw",
        tabmargins=[5, 5, 5, 5],
    )

    style.configure(
        "Subtab.TNotebook.Tab",
        background="lightblue",
        foreground="darkblue",
        padding=[5, 0],
        font=("Helvetica", 10, "bold"),
    )


def initialize_app(root):

    log_widget = setup_logging_frame(root)
    state = AppState(log_widget)
    state.root = root

    state.defaultextension = ".bnote"
    state.filetypes = [("BNOTE files", "*.bnote")]

    # ## 팀스탠다드 자동 임포트
    # load_from_json(state, "resource/PlantArch_BIM Standard.bnote")

    root.title("H_BimNote")
    root.geometry("1400x900+100+100")
    root.state("zoomed")

    define_styles()

    menubar = Menu(root)
    root.config(menu=menubar)

    # 파일 메뉴 추가
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(
        label="Save Team Standard", command=lambda: save_to_json_teamStdInfo(state)
    )  # save_to_json)
    file_menu.add_command(
        label="Load from BNOTE", command=lambda: load_from_json(state)
    )  # save_to_json)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    paned_window = tk.PanedWindow(
        root,
        orient=tk.HORIZONTAL,
    )
    paned_window.pack(expand=True, fill="both")

    notebook = ttk.Notebook(paned_window, style="Main.TNotebook")
    paned_window.add(notebook)

    return notebook, state
