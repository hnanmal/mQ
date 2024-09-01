# src/controllers/tree_controller.py

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
