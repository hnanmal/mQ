import tkinter as tk

from src.models.app_state import AppState


def initialize_app(logging_text_widget):
    state = AppState(logging_text_widget)
    state.project_info_ = tk.StringVar()
    return state
