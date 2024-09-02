# src/controllers/logic.py

from src.core.state_management import AppState
from src.models.wm_group import WMGroupManager
from src.controllers.clipboard_management import (
    copy_to_clipboard,
    # paste_from_clipboard,
    # paste_copied_items,
)


def initialize_app():
    state = AppState()
    wm_group_manager = WMGroupManager()
    state.update_wm_group_data(wm_group_manager.get_wm_group_data())
    return state, wm_group_manager


def lock_toggle_logic(state, wm_group_manager, item_name):
    state.set_lock_status(item_name, not state.get_lock_status(item_name))
    wm_group_manager.update_wm_group_data(item_name, state.wm_group_data.get(item_name))
    wm_group_manager.save()


def copy_selected_items(selected_items):
    """Copy the selected items to the clipboard."""
    copy_to_clipboard(selected_items)


# def paste_items(destination):
#     """Paste the items from the clipboard to the destination."""
#     clipboard_items = paste_from_clipboard()
#     if clipboard_items:
#         paste_copied_items(destination, clipboard_items)
