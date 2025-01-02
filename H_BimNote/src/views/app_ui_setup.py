import tkinter as tk
from tkinter import (
    # ttk,
    Menu,
)
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
        # tabmargins=[5, 5, 5, 5],
    )  # space around tabs

    style.configure(
        "Main.TNotebook.Tab",
        background="white",
        foreground="black",
        padding=[70, 0],
        # font=("Helvetica", 12, "bold"),
        font=("Arial", 12, "normal"),
    )

    # Define a custom style for the subtabs
    style.configure(
        "Subtab.TNotebook",
        tabposition="nw",
        # tabmargins=[5, 5, 5, 5],
    )

    style.configure(
        "Subtab.TNotebook.Tab",
        background="lightblue",
        foreground="darkblue",
        # padding=[50, 0],
        font=("Arial", 11, "normal"),
    )
    style.configure("lefttab.TNotebook", tabposition="wn")


def initialize_app(root):

    log_widget = setup_logging_frame(root)
    state = AppState(log_widget)
    state.root = root

    state.defaultextension = ".bnote"
    state.filetypes = [("BNOTE files", "*.bnote")]

    root.title("H_BimNote")
    root.geometry("1400x900+100+100")
    root.state("zoomed")

    define_styles()

    state.tab_bootStyle = "secondary"

    menubar = Menu(root)
    root.config(menu=menubar)

    # 파일 메뉴 추가
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(
        label="Save Team Standard as BNOTE  (Ctrl+S)",
        command=lambda: save_to_json_teamStdInfo(state),
    )  # save_to_json)
    file_menu.add_command(
        label="Load Team Standard from BNOTE  (Ctrl+L)",
        command=lambda: load_from_json(state),
    )  # save_to_json)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    paned_window = tk.PanedWindow(
        root,
        orient=tk.HORIZONTAL,
    )
    paned_window.pack(expand=True, fill="both")

    notebook = ttk.Notebook(
        paned_window,
        # style="Main.TNotebook",
        bootstyle=state.tab_bootStyle,
    )
    paned_window.add(notebook)

    # Ctrl+S 단축키를 'Save Team Standard' 기능에 연결
    root.bind("<Control-s>", lambda e: save_to_json_teamStdInfo(state))
    root.bind("<Control-l>", lambda e: load_from_json(state))

    # print("starting log widget\n")
    state.log_widget.write("starting log widget\n")

    return notebook, state
