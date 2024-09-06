# src/core/event_handling.py


def handle_tab_switch(state, new_tab_name):
    state.set_current_tab(new_tab_name)
    # Add any additional logic if needed


def handle_lock_toggle(state, item_name):
    current_status = state.get_lock_status(item_name)
    state.set_lock_status(item_name, not current_status)
    # Add additional logic to handle UI updates or data saving
