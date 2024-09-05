# src/controllers/logic.py

from src.core.state_management import AppState
from src.models.wm_group import WMGroupManager


def initialize_app(logging_text_widget):
    state = AppState(logging_text_widget)
    wm_group_manager = WMGroupManager()
    state.update_wm_group_data(wm_group_manager.get_wm_group_data())
    return state, wm_group_manager


def lock_toggle_logic(state, wm_group_manager, item_name):
    state.set_lock_status(item_name, not state.get_lock_status(item_name))
    wm_group_manager.update_wm_group_data(item_name, state.wm_group_data.get(item_name))
    wm_group_manager.save()
