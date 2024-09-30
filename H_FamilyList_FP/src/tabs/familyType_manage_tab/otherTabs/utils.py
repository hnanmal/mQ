def find_stdType_items_inCat(cat):
    def find_level_5_items(
        node,
        level=1,
    ):
        # Initialize an empty list to store level 5 items
        level_5_items = []

        # Check if the current node is a level 5 item by counting dots in 'number'
        if node.get("number", "").count(".") == 4:
            level_5_items.append(
                {
                    "name": node.get("name"),
                    "number": node.get("number"),
                    "description": node.get("description"),
                }
            )

        # If the node has children, iterate over them and recurse
        if "children" in node:
            for child in node["children"]:
                level_5_items.extend(find_level_5_items(child, level + 1))

        return level_5_items

    lv_5_items = []
    for root_node in state.stdTypes_info:
        if root_node["name"] == cat:
            lv_5_items.extend(find_level_5_items(root_node))
    return lv_5_items
