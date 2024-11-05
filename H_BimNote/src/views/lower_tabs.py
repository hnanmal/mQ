import tkinter as tk
from tkinter import ttk

from src.views.tksheet.sheet_utils import create_tksheet


def create_wmGrp_tab(state, subtab_notebook):
    g_wm_tab = ttk.Frame(subtab_notebook)
    subtab_notebook.add(g_wm_tab, text="Standard Work Master Group (G-WM)")

    paned_window = tk.PanedWindow(
        g_wm_tab,
        orient=tk.HORIZONTAL,
        sashwidth=7,
        bg="#e3e3e3",
    )
    paned_window.pack(expand=True, fill="both")

    section1 = ttk.Frame(
        g_wm_tab,
        width=700,
        height=2000,
    )

    section2 = ttk.Frame(
        g_wm_tab,
        width=700,
        height=2000,
    )

    paned_window.add(section1)
    paned_window.add(section2)

    # Place tksheet in G-WM tab
    GWM_sheet = create_tksheet(
        state,
        section1,
        headers=state.GWM_headers,
        data=[
            [1, 2],
            [1, 2],
        ],
        tab_name=None,
        height=2000,
        width=600,
        mode=None,
    )

    GWM_sheet.pack(padx=5, pady=2, anchor="w")

    # Place tksheet in G-WM tab
    sheet2 = create_tksheet(
        state,
        section2,
        headers=state.GWM_headers,
        data=[
            [1, 32],
            [1, 32],
        ],
        tab_name=None,
        height=2000,
        width=600,
        mode=None,
    )

    sheet2.pack(padx=5, pady=2, anchor="w")

    return g_wm_tab
