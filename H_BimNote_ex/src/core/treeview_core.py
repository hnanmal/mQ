from copy import deepcopy
from src.controllers.event_controllers import dispatch_event
from src.views.treeview.tree_tag_manage import determine_tag_by_level
from src.views.styles import configure_tree_styles


def calculate_level(tree, item):
    """Calculate the level of an item in the hierarchy."""
    level = 0
    while tree.parent(item):
        item = tree.parent(item)
        level += 1
    return level


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


def insert_item_with_indentation(state, tree, parent, item_data, index):
    """Insert an item with proper indentation and styling based on its level."""
    heads = state.stdTypeTree_head
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
        values=[indented_name].extend(item_data.get(head, "") for head in heads),
        tags=(tag,),
    )

    # Recursively insert any children
    for child in item_data.get("children", []):
        insert_item_with_indentation(state, tree, new_item, child, "end")

    # Force a refresh to apply styles immediately
    tree.update_idletasks()

    return new_item


def extract_treeview_data(tree, item_id=None, heads=None):
    """Extract data from the Treeview to save in JSON format."""

    if heads:
        heads = heads
    else:
        heads = [tree.heading(col, "text") for col in tree["columns"]]

    def extract_items(item_id):
        item_values = tree.item(item_id, "values")
        print(item_values)
        item_data = {
            "number": tree.item(item_id, "text"),
            "children": [],
        }
        for idx, head in enumerate(heads):
            if idx == 0:
                item_data[head] = item_values[0].strip()
            else:
                item_data[head] = item_values[idx]
        # item_data = {
        #     "number": tree.item(item_id, "text"),  # Save the number
        #     "name": item_values[0].strip(),  # Strip any indentation before saving
        #     "description": item_values[1],  # Save the description as is
        #     # "children": [],
        # }
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


def copy_treeview_items(state, tree, selected_items):
    """Copy selected items and their children."""
    copied_items = []
    for item in selected_items:
        # item_data = extract_treeview_data(tree, item)
        item_data = extract_treeview_data(tree, item, heads=state.stdTypeTree_heads)
        copied_items.append(item_data)
    return copied_items


def paste_treeview_items(state, tree, target_item, copied_items):
    """Paste copied items as children of the target item."""
    print(f"Pasting items to target: {target_item}")  # 디버깅 로그 추가
    for item_data in copied_items:
        # print(f"item_data: {item_data}")
        print(
            # f"Inserting item {item_data['name']} under {target_item}"
            f"item_data: {item_data}, type: {type(item_data)}"
        )  # 디버깅 로그 추가
        insert_item_with_indentation(state, tree, target_item, item_data, "end")
    renumber_treeview_items(tree, target_item)


def add_item(tree, state, heads=None):
    # from src.controllers.event_controllers import dispatch_event

    """Add a new item to the tree view with proper indentation based on its level."""
    logging_text_widget = state.logging_text_widget
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
    values_ = [indented_name]
    values_.extend("" for head in heads[1:])
    # Insert the new item under the selected parent with the indented name
    new_item = tree.insert(
        parent,
        "end",
        values=values_,
        tags=(tag,),
    )

    # Apply styles after adding the item
    configure_tree_styles(tree)
    tree.update_idletasks()

    # Expand the parent to show the new child
    tree.item(parent, open=True)

    # Push the operation to the undo stack
    state.undo_stack.append(("remove", new_item))

    dispatch_event(
        "ADD_ITEM",
        state,
        {"tree": tree, "item": new_item, "logging_widget": logging_text_widget},
    )


def remove_item(tree, state, item=None):
    # from src.controllers.event_controllers import dispatch_event

    """Remove the selected items from the Treeview based on the highest level and renumber the remaining items."""
    logging_text_widget = state.logging_text_widget
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
    ## dispatch for logging
    dispatch_event(
        "REMOVE_ITEM",
        state,
        {
            "tree": tree,
            "item": deepcopy(items_to_delete),
            "logging_widget": logging_text_widget,
        },
    )

    # Collect all undo operations in a list
    undo_operations = []

    # Sort items to ensure proper handling of hierarchical deletions
    items_to_delete = sorted(
        items_to_delete, key=lambda item: tree.index(item), reverse=True
    )

    for item_id in items_to_delete:
        parent_id = tree.parent(item_id)
        item_data = extract_treeview_data(tree, item_id, heads=state.stdTypeTree_heads)

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
    state.undo_stack.append(("batch_remove", undo_operations))


def undo_operation(state, tree):
    """Undo the last operation performed on the tree view."""
    if not state.undo_stack:
        print("Nothing to undo.")
        return

    last_operation = state.undo_stack.pop()

    if last_operation[0] == "remove":
        tree.delete(last_operation[1])

    elif last_operation[0] == "add":
        parent_id, item_data, item_index = (
            last_operation[1],
            last_operation[2],
            last_operation[3],
        )
        new_item = insert_item_with_indentation(
            state, tree, parent_id, item_data, item_index
        )

        # Reapply the tags
        item_level = calculate_level(tree, new_item)
        tag = determine_tag_by_level(item_level)
        tree.item(new_item, tags=(tag,))

    elif last_operation[0] == "batch_remove":
        # Handle batch removal undo
        undo_operations = last_operation[1]
        for operation in undo_operations:
            parent_id, item_data, item_index = operation[1], operation[2], operation[3]
            new_item = insert_item_with_indentation(
                state, tree, parent_id, item_data, item_index
            )

            # Reapply the tags
            item_level = calculate_level(tree, new_item)
            tag = determine_tag_by_level(item_level)
            tree.item(new_item, tags=(tag,))

    renumber_treeview_items(tree, parent_id)
