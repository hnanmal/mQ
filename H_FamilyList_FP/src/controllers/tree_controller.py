# src/controllers/tree_controller.py
from tkinter import messagebox

# from src.views.treeview_utils import swap_items, move_item
from src.controllers.event_dispatcher import dispatch_event
from src.views.styles import configure_styles
from src.utils.tree_utils import (
    determine_tag_by_level,
    renumber_treeview_items,
    calculate_level,
    # confirm_level_change,
    # move_item,
    # swap_items,
)

# Stack to keep track of operations for undo functionality
undo_stack = []

# Include other functions for adding, removing, undoing, saving, loading, etc.


def on_item_select(event, state, logging_text_widget):
    tree = event.widget
    selected_item = tree.selection()[0]
    dispatch_event(
        "ITEM_SELECT",
        state,
        {"tree": tree, "item": selected_item, "logging_widget": logging_text_widget},
    )


def add_item(tree):
    """Add a new item to the tree view with proper indentation based on its level."""
    selected_item = tree.selection()

    # Determine the parent for the new item
    if selected_item:
        parent = selected_item[0]  # Get the ID of the selected item
    else:
        parent = ""  # Insert at the top level if no item is selected

    # Calculate the level of the new item
    level = calculate_level(tree, parent)

    # Determine the appropriate tag based on the level
    tag = determine_tag_by_level(level)

    # Get the current number of children for the selected parent to determine the new item's number
    children = tree.get_children(parent)
    new_item_number = len(children) + 1
    new_item_text = f"Item {new_item_number}"

    # Apply indentation based on the level
    indented_name = "  " * (level + 1) + new_item_text

    # Insert the new item under the selected parent with the indented name
    new_item = tree.insert(
        parent, "end", values=(indented_name, "New Description"), tags=(tag,)
    )

    # Apply styles after adding the item
    configure_styles(tree)
    tree.update_idletasks()

    # Expand the parent to show the new child
    tree.item(parent, open=True)

    # Push the operation to the undo stack
    undo_stack.append(("remove", new_item))


def remove_item(tree):
    """Remove the selected items from the Treeview based on the highest level and renumber the remaining items."""
    selected_items = tree.selection()
    if not selected_items:
        return

    # Find the highest level item (closest to the root)
    highest_level_item = min(
        selected_items, key=lambda item: calculate_level(tree, item)
    )
    highest_level = calculate_level(tree, highest_level_item)

    # Filter out items that are children of other selected items
    items_to_delete = [
        item for item in selected_items if calculate_level(tree, item) == highest_level
    ]

    # Collect all undo operations in a list
    undo_operations = []

    # Sort items to ensure proper handling of hierarchical deletions
    items_to_delete = sorted(
        items_to_delete, key=lambda item: tree.index(item), reverse=True
    )

    for item_id in items_to_delete:
        parent_id = tree.parent(item_id)
        item_data = extract_treeview_data(tree, item_id)

        # Get the index of the item among its siblings
        siblings = tree.get_children(parent_id)
        item_index = siblings.index(item_id)

        # Debugging: Print details before deletion
        print(
            f"Removing Item ID: {item_id}, Parent ID: {parent_id}, Siblings: {siblings}, Item Index: {item_index}"
        )

        tree.delete(item_id)

        # Store the operation in the undo operations list
        undo_operations.append(("add", parent_id, item_data, item_index))

    # Renumber siblings to maintain order without touching the names
    renumber_treeview_items(tree, parent_id)

    # Push all undo operations to the stack as a single action
    undo_stack.append(("batch_remove", undo_operations))

    # Debugging: Print stack after removal
    print(f"Undo Stack: {undo_stack}")


def undo_operation(tree):
    """Undo the last operation performed on the tree view."""
    if not undo_stack:
        print("Nothing to undo.")
        return

    last_operation = undo_stack.pop()

    if last_operation[0] == "remove":
        tree.delete(last_operation[1])

    elif last_operation[0] == "add":
        parent_id, item_data, item_index = (
            last_operation[1],
            last_operation[2],
            last_operation[3],
        )
        new_item = insert_item_with_indentation(tree, parent_id, item_data, item_index)

        # Reapply the tags
        item_level = calculate_level(tree, new_item)
        tag = determine_tag_by_level(item_level)
        tree.item(new_item, tags=(tag,))
        # if item_level == 0:
        #     tree.item(new_item, tags=("Level0",))
        # elif item_level == 4:
        #     tree.item(new_item, tags=("Level4",))
        # else:
        #     tree.item(new_item, tags=("OtherLevels",))

    elif last_operation[0] == "batch_remove":
        # Handle batch removal undo
        undo_operations = last_operation[1]
        for operation in undo_operations:
            parent_id, item_data, item_index = operation[1], operation[2], operation[3]
            new_item = insert_item_with_indentation(
                tree, parent_id, item_data, item_index
            )

            # Reapply the tags
            item_level = calculate_level(tree, new_item)
            tag = determine_tag_by_level(item_level)
            tree.item(new_item, tags=(tag,))
            # if item_level == 0:
            #     tree.item(new_item, tags=("Level0",))
            # elif item_level == 4:
            #     tree.item(new_item, tags=("Level4",))
            # else:
            #     tree.item(new_item, tags=("OtherLevels",))


def insert_item_with_indentation(tree, parent, item_data, index):
    """Insert an item with proper indentation and styling based on its level."""
    # Calculate the level by counting the number of parents in the hierarchy
    level = calculate_level(tree, parent)

    # Add indentation to the name based on the level
    indented_name = "  " * (level + 1) + item_data["name"]

    # Determine the appropriate style based on the level
    tag = determine_tag_by_level(level)

    # Insert the item at the specified index with the style tag
    new_item = tree.insert(
        parent,
        index,
        text=item_data["number"],
        values=(indented_name, item_data["description"]),
        tags=(tag,),
    )

    # Recursively insert any children
    for child in item_data.get("children", []):
        insert_item_with_indentation(tree, new_item, child, "end")

    # Force a refresh to apply styles immediately
    tree.update_idletasks()

    return new_item


def extract_treeview_data(tree, item_id=None):
    """Extract data from the Treeview to save in JSON format."""

    def extract_items(item_id):
        item_values = tree.item(item_id, "values")
        item_data = {
            "number": tree.item(item_id, "text"),  # Save the number
            "name": item_values[0].strip(),  # Strip any indentation before saving
            "description": item_values[1],  # Save the description as is
        }
        children = tree.get_children(item_id)
        if children:
            item_data["children"] = [extract_items(child) for child in children]
        return item_data

    if item_id:
        return extract_items(item_id)
    else:
        root_items = tree.get_children("")
        return [extract_items(item) for item in root_items]
