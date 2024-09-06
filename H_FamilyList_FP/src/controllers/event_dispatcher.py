# src/controllers/event_dispatcher.py

from src.core.event_handling import handle_tab_switch, handle_lock_toggle

from src.views.drag_and_drop import (
    on_drag_motion,
    on_drag_release,
    on_drag_start,
)
from src.views.logging_utils import log_event_add, log_event_remove, log_event_selection


def dispatch_event(event_type, state, data=None):

    if event_type == "LOCK_TOGGLE":
        handle_lock_toggle(state, data)
    elif event_type == "DRAG_START":
        on_drag_start(data["tree"], data["event"])
    elif event_type == "DRAG_MOTION":
        on_drag_motion(data["tree"], data["event"])
    elif event_type == "DRAG_RELEASE":
        on_drag_release(data["tree"], data["event"])
    elif event_type == "ITEM_SELECT":
        log_event_selection(data["tree"], data["item"], data["logging_widget"])
    elif event_type == "ADD_ITEM":
        log_event_add(data["tree"], data["item"], data["logging_widget"])
    elif event_type == "REMOVE_ITEM":
        log_event_remove(data["tree"], data["item"], data["logging_widget"])

    # Add more event handlers as needed
