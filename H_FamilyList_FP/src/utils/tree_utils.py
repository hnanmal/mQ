# src/utils/tree_utils.py


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
