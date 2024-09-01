# src/controllers/tree_controller.py
from tkinter import messagebox
from src.views.treeview_utils import swap_items, move_item

# Variables to track drag start and end positions
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

def confirm_level_change():
    """Prompt the user to confirm the level change."""
    return messagebox.askokcancel("확인", "선택한 항목의 레벨이 변경됩니다. 이동하시겠습니까?")

def calculate_level(tree, item):
    """Calculate the level of an item in the hierarchy."""
    level = 0
    while tree.parent(item):
        item = tree.parent(item)
        level += 1
    return level

def insert_item_with_indentation(tree, parent, item_data, index):
    """Insert an item with proper indentation and styling based on its level."""
    # Calculate the level by counting the number of parents in the hierarchy
    level = calculate_level(tree, parent)
    
    # Add indentation to the name based on the level
    indented_name = '  ' * (level + 1) + item_data['name']
    
    # Determine the appropriate style based on the level
    if level == 1:
        tag = "Level1"
    elif level == 4:
        tag = "Level4"
    else:
        tag = "OtherLevels"
    
    # Insert the item at the specified index with the style tag
    new_item = tree.insert(parent, index, text=item_data['number'], values=(indented_name, item_data['description']), tags=(tag,))
    
    # Recursively insert any children
    for child in item_data.get('children', []):
        insert_item_with_indentation(tree, new_item, child, 'end')
    
    # Force a refresh to apply styles immediately
    tree.update_idletasks()

    return new_item


def apply_styles(tree):
    """Apply styles to all items in the tree based on their level."""
    for item in tree.get_children():
        apply_style_to_item(tree, item)

def apply_style_to_item(tree, item):
    """Apply a specific style to an item based on its level."""
    level = calculate_level(tree, item)
    if level == 1:
        tree.item(item, tags=("Level1",))
    elif level == 4:
        tree.item(item, tags=("Level4",))
    else:
        tree.item(item, tags=("OtherLevels",))
    
    # Recursively apply styles to children
    for child in tree.get_children(item):
        apply_style_to_item(tree, child)

# Include other functions for adding, removing, undoing, saving, loading, etc.
