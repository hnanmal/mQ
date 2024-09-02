# src/views/dialog_helpers.py

from tkinter import messagebox

def confirm_level_change():
    return messagebox.askokcancel("Confirm", "The level of the selected item will change. Do you want to proceed?")