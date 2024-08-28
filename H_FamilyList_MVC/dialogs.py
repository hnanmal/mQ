# Version: 1.0.0
import tkinter as tk
from tkinter import simpledialog, ttk


class ColumnSelectionDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Select Column")
        ttk.Label(master, text="Paste into which column?").pack()
        self.selection = tk.StringVar(value="Item")
        ttk.Radiobutton(
            master, text="Item", variable=self.selection, value="Item"
        ).pack(anchor="w")
        ttk.Radiobutton(
            master, text="Description", variable=self.selection, value="Description"
        ).pack(anchor="w")
        return None

    def apply(self):
        self.result = self.selection.get()
