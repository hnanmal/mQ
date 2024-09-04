# src/utils/tree_utils.py
import tkinter as tk


def enable_tree_item_editing(tree, item, column):
    """Enable editing for the specified column of the treeview item."""
    x, y, width, height = tree.bbox(item, column)
    entry = tk.Entry(tree, width=width)

    # Get the current text in the cell
    current_value = tree.item(item, "values")[int(column[1:]) - 1]

    entry.insert(0, current_value)
    entry.place(x=x, y=y, width=width, height=height)

    def save_edit(event):
        new_value = entry.get()
        tree.set(item, column=column, value=new_value)
        entry.destroy()

    entry.bind("<Return>", save_edit)
    entry.bind("<FocusOut>", lambda event: entry.destroy())
    entry.focus()


def determine_tag_by_level(level):
    """Determine the appropriate tag based on the level of the TreeView item."""
    lv_1st = 0
    lv_2nd = 4

    if level == lv_1st:
        return f"Level{lv_1st}"
    elif level == lv_2nd:
        return f"Level{lv_2nd}"
    else:
        return "OtherLevels"


def renumber_treeview_items(tree, parent=""):
    """Renumber only the sibling items under the specified parent."""

    # Determine the starting number based on the parent's level
    if parent == "":
        start_number = 0  # Root level starts at 0
    else:
        start_number = 1  # All other levels start at 1

    for i, item in enumerate(tree.get_children(parent), start=start_number):
        # Construct the new hierarchical number
        parent_number = tree.item(parent, "text") if parent else ""
        new_number = f"{parent_number}.{i}" if parent_number else str(i)

        # Get the current values of the item (Name, Description)
        current_values = tree.item(item, "values")

        # Preserve Name and Description
        current_name = (
            current_values[0] if len(current_values) > 0 else ""
        )  # Keep the Name as is
        current_description = (
            current_values[1] if len(current_values) > 1 else ""
        )  # Keep the Description as is

        # Update the 'text' attribute with the hierarchical number
        tree.item(item, text=new_number)

    # No recursive call here since we're only renumbering siblings, not their children


def calculate_level(tree, item):
    """Calculate the level of an item in the hierarchy."""
    level = 0
    while tree.parent(item):
        item = tree.parent(item)
        level += 1
    return level


def confirm_level_change():
    """Prompt the user to confirm the level change."""
    from tkinter import messagebox

    return messagebox.askokcancel(
        "확인", "선택한 항목의 레벨이 변경됩니다. 이동하시겠습니까?"
    )


def move_item(tree, item, new_parent, sibling):
    """Move the item to a new parent, above the given sibling."""
    tree.move(item, new_parent, tree.index(sibling))
    renumber_treeview_items(tree, new_parent)
    renumber_treeview_items(tree, tree.parent(item))  # Renumber original parent


def swap_items(tree, item1, item2):
    """Swap the positions of two items in the same parent."""
    parent = tree.parent(item1)
    index1 = tree.index(item1)
    index2 = tree.index(item2)
    tree.move(item1, parent, index2)
    tree.move(item2, parent, index1)
    renumber_treeview_items(tree, parent)


def extract_treeview_data(tree, item_id=None):
    """Extract data from the Treeview to save in JSON format."""

    def extract_items(item_id):
        item_values = tree.item(item_id, "values")
        item_data = {
            "number": tree.item(item_id, "text"),  # Save the number
            "name": item_values[0].strip(),  # Strip any indentation before saving
            "description": item_values[1],  # Save the description as is
            # "children": [],
        }
        children = tree.get_children(item_id)
        if children:
            item_data["children"] = [extract_items(child) for child in children]
        return item_data

    if item_id:
        print(f"Extracting data for item_id: {item_id}")  # 디버깅 메시지 추가
        return extract_items(item_id)
    else:
        root_items = tree.get_children("")
        return [extract_items(item) for item in root_items]


def copy_treeview_items(tree, selected_items):
    """Copy selected items and their children."""
    copied_items = []
    for item in selected_items:
        # item_data = extract_treeview_data(tree, item)
        item_data = extract_treeview_data(tree, item)
        copied_items.append(item_data)
    return copied_items


def paste_treeview_items(tree, target_item, copied_items):
    """Paste copied items as children of the target item."""
    print(f"Pasting items to target: {target_item}")  # 디버깅 로그 추가
    for item_data in copied_items:
        # print(f"item_data: {item_data}")
        print(
            # f"Inserting item {item_data['name']} under {target_item}"
            f"item_data: {item_data}, type: {type(item_data)}"
        )  # 디버깅 로그 추가
        insert_item_with_indentation(tree, target_item, item_data, "end")
    renumber_treeview_items(tree, target_item)


def insert_item_with_indentation(tree, parent, item_data, index):
    """Insert an item with proper indentation and styling based on its level."""

    # item_data 디버깅 출력
    print(f"Inserting item_data: {item_data}, type: {type(item_data)}")

    # Calculate the level by counting the number of parents in the hierarchy
    level = calculate_level(tree, parent)

    # 예상한 item_data 구조가 맞는지 확인
    if isinstance(item_data, dict) and "name" in item_data:
        indented_name = "  " * (level + 1) + item_data["name"]
    else:
        raise ValueError(f"Invalid item_data format: {item_data}")

    # Add indentation to the name based on the level
    indented_name = "  " * (level + 1) + item_data["name"]

    # Determine the appropriate style based on the level
    tag = determine_tag_by_level(level)

    # Debugging: Check if the tree is getting the correct item and parent
    print(f"Parent: {parent}, Index: {index}, Indented Name: {indented_name}")

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
