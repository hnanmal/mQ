import tkinter as tk
import tkinter.font
from tkinter import ttk


def create_listbox(state, frame):
    # Create a frame to hold the Listbox and scrollbar
    listbox_frame = ttk.Frame(frame)
    listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create Listbox
    listbox = tk.Listbox(
        listbox_frame,
        selectmode=tk.EXTENDED,  # Allow multiple selections
        bg="white",  # Background color
        fg="black",  # Text color
        font=("Arial", 11),  # Font customization
        activestyle="none",
        selectbackground="green",  # Highlight background color
        selectforeground="white",  # Highlight text color
        # highlightthickness=0,
        width=60,
        height=50,
    )  # Width and height of Listbox

    # Add Scrollbar
    scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Connect Scrollbar to Listbox
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    listbox.pack(side=tk.TOP, fill=tk.BOTH)

    for i in range(1, 200):
        listbox.insert(tk.END, i)

    return listbox
