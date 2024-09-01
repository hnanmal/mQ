# src/controllers/event_dispatcher.py
from src.core.event_handling import handle_tab_switch, handle_lock_toggle

def dispatch_event(event_type, state, data=None):
    if event_type == "TAB_SWITCH":
        handle_tab_switch(state, data)
    elif event_type == "LOCK_TOGGLE":
        handle_lock_toggle(state, data)
    # Add more event handlers as needed