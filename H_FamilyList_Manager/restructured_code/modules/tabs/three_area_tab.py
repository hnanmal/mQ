# modules/tabs/three_area_tab.py

import tkinter as tk
from tkinter import ttk

def create_three_area_tab(app, name):
    # Create a frame for the tab
    tab_frame = ttk.Frame(app.notebook)

    # Create left, middle, and right frames
    left_frame = ttk.Frame(tab_frame)
    middle_frame = ttk.Frame(tab_frame)
    right_frame = ttk.Frame(tab_frame)

    # Left content
    left_label = ttk.Label(left_frame, text=f"Left content of {name}")
    left_button = ttk.Button(
        left_frame,
        text="Left Button",
        command=lambda: app.context_menu_manager.on_button_click(
            f"Left Button on {name}"
        ),
    )
    left_text = ttk.Entry(left_frame, width=30)

    # Middle content
    middle_label = ttk.Label(middle_frame, text=f"Middle content of {name}")
    middle_button = ttk.Button(
        middle_frame,
        text="Middle Button",
        command=lambda: app.context_menu_manager.on_button_click(
            f"Middle Button on {name}"
        ),
    )
    middle_text = ttk.Entry(middle_frame, width=30)

    # Right content
    right_label = ttk.Label(right_frame, text=f"Right content of {name}")
    right_button = ttk.Button(
        right_frame,
        text="Right Button",
        command=lambda: app.context_menu_manager.on_button_click(
            f"Right Button on {name}"
        ),
    )
    right_text = ttk.Entry(right_frame, width=30)

    # Pack left content with padding
    left_label.pack(padx=20, pady=10)
    left_button.pack(padx=20, pady=10)
    left_text.pack(padx=20, pady=10)

    # Pack middle content with padding
    middle_label.pack(padx=20, pady=10)
    middle_button.pack(padx=20, pady=10)
    middle_text.pack(padx=20, pady=10)

    # Pack right content with padding
    right_label.pack(padx=20, pady=10)
    right_button.pack(padx=20, pady=10)
    right_text.pack(padx=20, pady=10)

    # Layout left, middle, and right frames
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    middle_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Add the tab to the notebook with increased padding
    app.notebook.add(tab_frame, text=f"   {name}   ")
