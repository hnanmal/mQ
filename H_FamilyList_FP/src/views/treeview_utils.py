# src/views/treeview_utils.py

import json
import os
from tkinter import filedialog

from src.controllers.tree_controller import *
from src.views.styles import configure_styles


search_state = {
    "last_search": None,
    "last_match": None
}

def search_treeview(tree, search_text):
    """Search the Treeview for items that match the search_text in the Name or Description."""
    global search_state
    items = tree.get_children('')
    
    # Flatten the tree to get a list of all items
    all_items = []
    def flatten_tree(parent):
        for item in tree.get_children(parent):
            all_items.append(item)
            flatten_tree(item)
    
    flatten_tree('')

    # If continuing from the last search, start after the last matched item
    start_index = 0
    if search_state["last_search"] == search_text and search_state["last_match"] is not None:
        start_index = all_items.index(search_state["last_match"]) + 1

    # Search for the next match
    for i in range(start_index, len(all_items)):
        item = all_items[i]
        item_values = tree.item(item, 'values')
        item_name = item_values[0] if len(item_values) > 0 else ""
        item_description = item_values[1] if len(item_values) > 1 else ""

        if search_text.lower() in item_name.lower() or search_text.lower() in item_description.lower():
            tree.selection_set(item)
            tree.see(item)
            search_state["last_search"] = search_text
            search_state["last_match"] = item
            return

    # If no match is found or the end of the tree is reached, reset the search
    search_state["last_search"] = None
    search_state["last_match"] = None
    print("No more matches found.")


# Stack to keep track of operations for undo functionality
undo_stack = []

def load_json_data(file_path):
    """Load JSON data from a file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("JSON data loaded successfully.")
            return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        return None

def save_json_data(file_path, data):
    """Save data to a JSON file with UTF-8 encoding."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print("Tree view data saved successfully.")
    except Exception as e:
        print(f"Error saving JSON: {e}")

def populate_treeview(tree, data, parent="", level=0):
    """Populate the Treeview widget with JSON data."""
    def insert_items(parent, items, level):
        for item in items:
            # Add indentation based on the level
            indented_name = '  ' * level + item['name']
            node_id = tree.insert(parent, "end", text=item['number'], values=(indented_name, item.get('description', '')))
            children = item.get("children", [])
            if children:
                insert_items(node_id, children, level + 1)

    tree.delete(*tree.get_children())  # Clear the existing tree view
    insert_items(parent, data, level)

    # Force a refresh to apply styles
    configure_styles(tree)
    tree.update_idletasks()


def extract_treeview_data(tree, item_id=None):
    """Extract data from the Treeview to save in JSON format."""
    def extract_items(item_id):
        item_values = tree.item(item_id, 'values')
        item_data = {
            "number": tree.item(item_id, 'text'),  # Save the number
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



def renumber_treeview_items(tree, parent=""):
    """Renumber the items under the specified parent, updating the Number column to reflect the hierarchy."""
    parent_number = tree.item(parent, 'text') if parent else ""
    
    for i, item in enumerate(tree.get_children(parent), start=1):
        # Construct the new hierarchical number
        new_number = f"{parent_number}.{i}" if parent_number else str(i)

        # Get the current values of the item (Name, Description)
        current_values = tree.item(item, 'values')

        # Preserve Name and Description
        current_name = current_values[0] if len(current_values) > 0 else ""  # Keep the Name as is
        current_description = current_values[1] if len(current_values) > 1 else ""  # Keep the Description as is

        # Update the 'text' attribute with the hierarchical number
        tree.item(item, text=new_number)

        # Debugging: Print the updated values
        print(f"After renumbering: Item ID: {item}, New Number: {new_number}, Values: {current_values}")

        # Recursively renumber any children
        renumber_treeview_items(tree, item)

    configure_styles(tree)
    tree.update_idletasks()


def expand_or_collapse_tree(tree, level):
    """Expand or collapse tree view items up to the specified level."""
    def expand_children(item, current_level, target_level):
        if current_level < target_level:
            tree.item(item, open=True)
            children = tree.get_children(item)
            for child in children:
                expand_children(child, current_level + 1, target_level)
        else:
            tree.item(item, open=False)

    root_items = tree.get_children("")
    for item in root_items:
        expand_children(item, 1, level)

    configure_styles(tree)
    tree.update_idletasks()

def add_item(tree):
    """Add a new item to the tree view with proper indentation based on its level."""
    selected_item = tree.selection()
    
    # Determine the parent for the new item
    if selected_item:
        parent = selected_item[0]  # Get the ID of the selected item
    else:
        parent = ''  # Insert at the top level if no item is selected

    # Calculate the level of the new item
    level = calculate_level(tree, parent)
    
    # Get the current number of children for the selected parent to determine the new item's number
    children = tree.get_children(parent)
    new_item_number = len(children) + 1
    new_item_text = f"Item {new_item_number}"
    
    # Apply indentation based on the level
    indented_name = '  ' * (level + 1) + new_item_text

    # Insert the new item under the selected parent with the indented name
    new_item = tree.insert(parent, "end", values=(indented_name, "New Description"))

    # Apply styles after adding the item
    configure_styles(tree)
    tree.update_idletasks()

    # Expand the parent to show the new child
    tree.item(parent, open=True)

    # Push the operation to the undo stack
    undo_stack.append(('remove', new_item))


def remove_item(tree):
    """Remove the selected items from the Treeview based on the highest level and renumber the remaining items."""
    selected_items = tree.selection()
    if not selected_items:
        return

    # Find the highest level item (closest to the root)
    highest_level_item = min(selected_items, key=lambda item: calculate_level(tree, item))
    highest_level = calculate_level(tree, highest_level_item)

    # Filter out items that are children of other selected items
    items_to_delete = [
        item for item in selected_items 
        if calculate_level(tree, item) == highest_level
    ]

    # Collect all undo operations in a list
    undo_operations = []

    # Sort items to ensure proper handling of hierarchical deletions
    items_to_delete = sorted(items_to_delete, key=lambda item: tree.index(item), reverse=True)

    for item_id in items_to_delete:
        parent_id = tree.parent(item_id)
        item_data = extract_treeview_data(tree, item_id)
        
        # Get the index of the item among its siblings
        siblings = tree.get_children(parent_id)
        item_index = siblings.index(item_id)
        
        # Debugging: Print details before deletion
        print(f"Removing Item ID: {item_id}, Parent ID: {parent_id}, Siblings: {siblings}, Item Index: {item_index}")
        
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
        parent_id, item_data, item_index = last_operation[1], last_operation[2], last_operation[3]
        insert_item_with_indentation(tree, parent_id, item_data, item_index)
        renumber_treeview_items(tree, parent_id)

    elif last_operation[0] == "batch_remove":
        # Undo multiple deletions
        undo_operations = last_operation[1]
        # Sort undo operations to restore in the correct order
        undo_operations = sorted(undo_operations, key=lambda op: op[3])

        for operation in undo_operations:
            parent_id, item_data, item_index = operation[1], operation[2], operation[3]
            insert_item_with_indentation(tree, parent_id, item_data, item_index)
            renumber_treeview_items(tree, parent_id)
        
    # Force a refresh to apply styles immediately
    configure_styles(tree)
    tree.update_idletasks()



def calculate_level(tree, item):
    """Calculate the level of an item in the hierarchy."""
    level = 0
    while tree.parent(item):
        item = tree.parent(item)
        level += 1
    return level


def save_treeview(tree):
    """Save the current state of the tree view to a JSON file."""
    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if save_path:
        tree_data = extract_treeview_data(tree)
        save_json_data(save_path, tree_data)

def load_treeview(tree):
    """Load a new JSON file and populate the tree view."""
    load_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if load_path:
        new_data = load_json_data(load_path)
        if new_data:
            populate_treeview(tree, new_data)

def swap_items(tree, item1, item2):
    """Swap the positions of two items in the same parent."""
    parent = tree.parent(item1)
    index1 = tree.index(item1)
    index2 = tree.index(item2)
    tree.move(item1, parent, index2)
    tree.move(item2, parent, index1)
    renumber_treeview_items(tree, parent)

def move_item(tree, item, new_parent, sibling):
    """Move the item to a new parent, above the given sibling."""
    tree.move(item, new_parent, tree.index(sibling))
    renumber_treeview_items(tree, new_parent)
    renumber_treeview_items(tree, tree.parent(item))  # Renumber original parent
