# src/views/drag_and_drop.py

# Variables to track drag start and end positions
from src.utils.tree_utils import (
    calculate_level,
    confirm_level_change,
    move_item,
    swap_items,
)


drag_data = {"item": None, "start_parent": None}


def on_drag_start(tree, event):
    """Start the dragging process."""
    region = tree.identify("region", event.x, event.y)
    if region == "heading":
        return  # Prevent dragging from the header

    item = tree.identify_row(event.y)
    if item:
        drag_data["item"] = item
        drag_data["start_parent"] = tree.parent(item)


def on_drag_motion(tree, event):
    """Handle the dragging motion."""
    # Visual feedback can be implemented here (e.g., highlight the drop target)


def on_drag_release(tree, event):
    """Handle the drop and perform the move operation."""
    if not drag_data["item"]:
        return

    drop_item = tree.identify_row(event.y)
    if not drop_item:
        return

    start_item = drag_data["item"]
    start_parent = drag_data["start_parent"]
    end_parent = tree.parent(drop_item)

    if start_parent == end_parent:
        # Same parent: swap positions
        swap_items(tree, start_item, drop_item)
    else:
        # Different parents: prompt for level change if necessary
        start_level = calculate_level(tree, start_item)
        end_level = calculate_level(tree, drop_item)
        if start_level != end_level:
            if not confirm_level_change():
                return

        # Move the item to the new parent
        move_item(tree, start_item, end_parent, drop_item)

    # Clear drag data
    drag_data["item"] = None
    drag_data["start_parent"] = None
