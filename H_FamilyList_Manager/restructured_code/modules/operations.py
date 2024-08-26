# modules/operations.py

import tkinter as tk
from tkinter import messagebox


class WM_group_tab_CenterAreaOperations:
    def __init__(self, app):
        self.app = app

    def add_item_to_center(self):
        selected_items = self.app.excel_treeview.selection()
        if not selected_items:
            messagebox.showwarning(
                "No Selection", "Please select an item from the Excel data."
            )
            return
        for item in selected_items:
            item_text = self.app.excel_treeview.item(item, "values")[0]
            self.app.drop_area.insert(tk.END, item_text)

    def remove_item_from_center(self):
        selected_index = self.app.drop_area.curselection()
        if selected_index:
            self.app.drop_area.delete(selected_index)
