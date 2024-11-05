import tkinter as tk

from src.models.app_state import AppState


def initialize_app(logging_text_widget, root=None):
    state = AppState(logging_text_widget)
    state.root = root
    state.project_info_ = tk.StringVar()

    state.stdTypeTree_heads = [
        # "No",
        "StdType",
        "Description",
        "G-WM 1",
        "G-WM 2",
        "G-WM 3",
        "G-WM 4",
        "S-WM 1",
        "표준산출식",
    ]

    return state
