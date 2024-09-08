# src/controllers/logic.py

import tkinter as tk
from src.core.state_management import AppState
from src.models.wm_group import WMGroupManager


def initialize_app(logging_text_widget):
    state = AppState(logging_text_widget)
    wm_group_manager = WMGroupManager()
    state.update_wm_group_data(wm_group_manager.get_wm_group_data())
    return state, wm_group_manager

def lock_toggle_logic(state, wm_group_manager, item_name, center_listbox, add_button, del_button):
    is_locked = not state.get_lock_status(item_name)  # Toggle the lock status
    state.set_lock_status(item_name, is_locked)

    matched_items = center_listbox.get(0, tk.END)

    if is_locked:
        # Apply lock styles and disable the listbox and buttons
        center_listbox.config(state='normal', bg='#e2e2e2', fg='blue')  # Light gray background, blue text
        add_button.config(state='disabled')
        del_button.config(state='disabled')

        # Disable interaction
        center_listbox.bind('<Button-1>', lambda e: 'break')  # Prevent selection

        # Save the matching results into wm_group_match.json
        wm_group_manager.update_wm_group_data(item_name, list(matched_items), locked=True)

    else:
        # Reset to unlocked state
        center_listbox.config(state='normal', bg='white', fg='black')
        add_button.config(state='normal')
        del_button.config(state='normal')

        # Re-enable interaction
        center_listbox.unbind('<Button-1>')  # Re-enable selection

        # Save the matching results with lock status as False
        wm_group_manager.update_wm_group_data(item_name, list(matched_items), locked=False)

    wm_group_manager.save()
