from copy import deepcopy


class TreeDataManager:
    def __init__(self, state, related_widget=None):
        self.state = state
        self.team_std_info = state.team_std_info
        self.data_kind = related_widget.data_kind if related_widget else None

    def register_related_widget(self, related_widget):
        self.related_widget = related_widget

    def find_node_by_name(self, data, target_name):
        """Find a node by its name in the given children list."""
        return next(
            (
                node
                for node in data
                if isinstance(node, dict) and node["name"] == target_name
            ),
            None,
        )

    def find_node_by_name_recur(self, data, target_name):
        """Find a node by its name in the given tree structure recursively."""
        # If data is a list, iterate through each node
        if isinstance(data, list):
            for node in data:
                if isinstance(node, dict):
                    # If the current node matches the target name, return it
                    if node.get("name") == target_name:
                        return node

                    # If the current node has children, search within them recursively
                    if "children" in node:
                        found_node = self.find_node_by_name(
                            node["children"], target_name
                        )
                        if found_node:
                            return found_node
        return None

    def find_node_by_path(self, data, path):
        """Find a node by traversing the given path in the tree structure."""
        current_node = None
        for name in path:
            if isinstance(data, list):
                current_node = next(
                    (
                        node
                        for node in data
                        if isinstance(node, dict) and node.get("name") == name
                    ),
                    None,
                )
                if current_node is None:
                    return None
                data = current_node.get("children", [])
            else:
                return None
        return current_node

    def get_node_path(self, data_kind, grandparent_name, parent_name, child_name):
        """Navigate to the specified node based on grandparent, parent, and child names."""
        if data_kind not in self.team_std_info:
            return None, None, None

        # Navigate to the grandparent node
        data = self.team_std_info[data_kind]["children"]
        grandparent_node = self.find_node_by_name(data, grandparent_name)
        if not grandparent_node:
            return None, None, None

        # Navigate to the parent node
        parent_node = self.find_node_by_name(grandparent_node["children"], parent_name)
        if not parent_node:
            return None, None, None

        # Check if parent_node has children and if they are a list (last level)
        if isinstance(parent_node["children"], list) and all(
            isinstance(child, str) for child in parent_node["children"]
        ):
            return grandparent_node, parent_node, parent_node["children"]

        # Navigate to the selected child node
        child_node = self.find_node_by_name(parent_node["children"], child_name)
        return grandparent_node, parent_node, child_node

    def get_node_depth(self, node):
        """Calculate the depth of a given node in the tree data."""
        depth = 0
        while "parent" in node:
            depth += 1
            node = node["parent"]
        return depth

    def update_node_value(self, data_kind, path, column_index, new_value):
        """Update the value of a node in the tree."""
        selected_node = self.find_node_by_path(
            self.team_std_info[data_kind]["children"], path
        )

        if selected_node is not None and "values" in selected_node:
            # Ensure that the values list is long enough
            if len(selected_node["values"]) <= column_index:
                selected_node["values"].extend(
                    [""] * (column_index + 1 - len(selected_node["values"]))
                )

            # Update the corresponding value in "values"
            selected_node["values"][column_index] = new_value
            print(
                f"Updated node value: {selected_node['name']}, column {column_index} to {new_value}"
            )
        else:
            print(f"Could not find node '{path}' or 'values' key is missing.")

    def update_node_name(self, data_kind, path, new_name):
        """Update the name of a node in the tree."""
        selected_node = self.find_node_by_path(
            self.team_std_info[data_kind]["children"], path
        )

        if selected_node is not None:
            selected_node["name"] = new_name
            # Ensure that the name is also updated in the corresponding value at the level column index
            # depth = self.get_node_depth(selected_node)
            # if len(selected_node["values"]) > depth:
            #     selected_node["values"][depth] = new_name
            # print(f"Updated node name: {selected_node['name']} to {new_name}")
        else:
            print(f"Could not find node '{path}' to update name.")

    def add_top_level_node(self, data_kind, new_child):
        """Add a new top-level node to the specified data kind."""
        try:
            # Create the values list with empty strings, setting the name in the first column
            values = [new_child]

            # Append the new child to the top-level "children" list
            self.team_std_info[data_kind]["children"].append(
                {
                    "name": new_child,
                    "values": values,
                    "children": [],
                }
            )
            print(f"Added top-level node: {new_child}")
        except Exception as e:
            print(f"Error adding top-level node: {e}")

    def add_child_node(self, data_kind, selected_name, new_child):
        """Add a new child node to the specified selected node."""
        try:
            # Try to find the selected node at any level
            def find_node_recursive(data, target_name):
                if not isinstance(data, list):
                    return None
                for node in data:
                    if isinstance(node, dict) and node.get("name") == target_name:
                        return node
                    if "children" in node:
                        found_node = find_node_recursive(node["children"], target_name)
                        if found_node:
                            return found_node
                return None

            selected_node = find_node_recursive(
                self.team_std_info[data_kind]["children"], selected_name
            )

            if selected_node is not None and "children" in selected_node:

                # Determine the depth level of the selected node
                depth = selected_node["values"].index(selected_node["name"]) + 1

                # Create the values list with empty strings, setting the name in the appropriate column
                values = [""] * (depth + 1)
                values[depth] = new_child

                selected_node["children"].append(
                    {
                        "name": new_child,
                        "values": values,
                        "children": [],
                    }
                )
                print(f"Added child node: {new_child} to {selected_name}")
            else:
                print(
                    f"Could not find selected node '{selected_name}' or 'children' key is missing."
                )
        except Exception as e:
            print(f"Error adding child node: {e}")

    def delete_node(self, data_kind, path):
        """Delete the specified node from the tree based on its path."""
        try:
            # Helper function to find a node by traversing the path
            def find_node_by_path(data, path):
                current_node = None
                for name in path:
                    if isinstance(data, list):
                        current_node = next(
                            (node for node in data if node.get("name") == name), None
                        )
                        if current_node is None:
                            return None  # Stop if the node doesn't exist
                        data = current_node.get("children", [])
                    else:
                        return None  # If data is not a list, stop traversal
                return current_node

            # Validate the path
            if not path or not isinstance(path, list):
                print("Invalid path: Path must be a non-empty list of node names.")
                return

            if data_kind not in self.team_std_info:
                print(f"Invalid data kind: {data_kind}")
                return

            # Ensure the path includes the parent's path and the target node name
            parent_path = path[:-1]
            target_name = path[-1]

            # Find the parent node
            parent_node = find_node_by_path(
                self.team_std_info[data_kind]["children"], parent_path
            )

            if not parent_node or "children" not in parent_node:
                print(f"Could not find parent node for path: {parent_path}")
                return

            # Find the target node in the parent's children
            target_node = next(
                (
                    node
                    for node in parent_node["children"]
                    if node.get("name") == target_name
                ),
                None,
            )

            if not target_node:
                print(
                    f"Could not find target node '{target_name}' in the specified path."
                )
                return

            # Remove the target node from the parent's children
            parent_node["children"].remove(target_node)
            print(f"Deleted node: {target_name}")

        except Exception as e:
            print(f"Error deleting node: {e}")

    def copy_node(self, data_kind, path, new_name, name_depth):
        """Copy the selected node and its children, placing the copy directly below the original."""
        try:
            # Find the node by traversing the path
            def find_node_by_path(data, path):
                current_node = None
                for name in path:
                    if isinstance(data, list):
                        current_node = next(
                            (node for node in data if node.get("name") == name), None
                        )
                        if current_node is None:
                            return None
                        data = current_node.get("children", [])
                    else:
                        return None
                return current_node

            # Ensure the path includes the parent's path and the target node name
            parent_path = path[:-1]
            target_name = path[-1]

            # Find the parent node
            parent_node = find_node_by_path(
                self.team_std_info[data_kind]["children"], parent_path
            )

            if not parent_node or "children" not in parent_node:
                print(f"Could not find the parent node for path: {parent_path}")
                return

            # Find the target node in the parent's children
            selected_node = next(
                (
                    node
                    for node in parent_node["children"]
                    if node.get("name") == target_name
                ),
                None,
            )

            if not selected_node:
                print(f"Could not find the node '{target_name}' to copy.")
                return

            # Create a deep copy of the selected node
            def deep_copy_node(node, new_name=None):
                """Deep copy a node, renaming it if a new_name is provided."""
                # Determine the depth level of the selected node
                depth = node["values"].index(node["name"])

                new_values = node["values"][:]
                # if depth == 1:
                if depth == name_depth:
                    new_values[depth] = new_name

                copied_node = {
                    "name": new_name if new_name else node["name"],
                    # "values": node["values"][:],  # Copy values
                    "values": new_values,  # Copy values
                }

                # Check if the node has children
                if "children" in node:
                    if isinstance(node["children"], list):
                        # Check if children are tree nodes or simple items
                        if all(isinstance(child, dict) for child in node["children"]):
                            # Deep copy child tree nodes
                            copied_node["children"] = [
                                deep_copy_node(child) for child in node["children"]
                            ]
                        else:
                            # Directly copy the list of items
                            copied_node["children"] = node["children"][:]
                    else:
                        # If children is not a list, handle it gracefully
                        copied_node["children"] = []

                return copied_node

            # Generate a deep copy with a new name
            copied_node = deep_copy_node(selected_node, new_name)

            # Insert the copied node directly after the selected node in the parent's children
            index = parent_node["children"].index(selected_node)
            parent_node["children"].insert(index + 1, copied_node)
            print(f"Copied node '{target_name}' to '{new_name}'.")

        except Exception as e:
            print(f"Error copying node: {e}")


class TreeDataManager_treeview(TreeDataManager):
    def __init__(self, state, related_widget=None):
        super().__init__(state, related_widget=related_widget)

    def match_wms_to_stdType(
        self, data_kind, grandparent_name, parent_name, child_name, selected_wms
    ):
        """Add specified matched WMs to the children of the selected node."""
        _, parent_node, selected_node = self.get_node_path(
            data_kind, grandparent_name, parent_name, child_name
        )

        if isinstance(selected_node, list) and selected_wms:
            # Handle adding to list of strings (last level)
            print(f"Adding matched WMs: {selected_wms}")
            parent_node["children"].extend(selected_wms)
        elif selected_node and "children" in selected_node and selected_wms:
            # Handle adding matched WMs to regular children
            print(f"Adding matched WMs: {selected_wms}")
            selected_node["children"].extend(selected_wms)

    def remove_matched_wms(
        self, data_kind, grandparent_name, parent_name, child_name, matched_wms
    ):
        """Remove specified matched WMs from the children of the selected node."""
        _, parent_node, selected_node = self.get_node_path(
            data_kind, grandparent_name, parent_name, child_name
        )

        if isinstance(selected_node, list):
            # Handle removal from list of strings (last level)
            print(f"Removing matched WMs: {matched_wms}")
            parent_node["children"] = [
                child for child in selected_node if child not in matched_wms
            ]
        elif selected_node and "children" in selected_node:
            # Handle removal from regular children
            print(f"Removing matched WMs: {matched_wms}")
            selected_node["children"] = [
                child for child in selected_node["children"] if child not in matched_wms
            ]

    def match_GWMitems_to_stdFam(
        self, data_kind, grandparent_name, parent_name, child_name, selected_GWMitems
    ):
        """Add specified matched WMs to the children of the selected node, recognizing derived items by inclusion."""
        _, parent_node, selected_node = self.get_node_path(
            data_kind, grandparent_name, parent_name, child_name
        )
        selected_GWMitems_copy = deepcopy(selected_GWMitems)

        # Get existing child names for recognition of derivatives
        existing_names = {child["name"] for child in selected_node.get("children", [])}

        for selected_GWMitem in selected_GWMitems_copy:
            # Check if the item is a derivative by inclusion
            base_name = selected_GWMitem["name"]
            derived_from = next(
                (name for name in existing_names if base_name.startswith(name)), None
            )

            if derived_from:
                # Recognized as a derived item, update its name to include base name
                selected_GWMitem["name"] = (
                    base_name  # The name already represents the derived item
                )

            # Update the values for the item
            new_values = list(selected_GWMitem["values"])
            new_values.insert(0, "")  # Add placeholders for columns
            new_values.insert(0, "")
            new_values.insert(0, "")
            selected_GWMitem.update({"values": new_values})

            # Copy formulas for the children if they match a reference item
            children = list(selected_GWMitem.get("children", []))
            reference_item = (
                selected_node.get("children", [])
                if isinstance(selected_node, dict)
                else []
            )[0]
            for child in children:
                # Find a matching reference child by name
                matching_reference = next(
                    (
                        ref
                        for ref in reference_item["children"]
                        if ref["name"] == child["name"]
                    ),
                    None,
                )

                # Copy formula from the matching reference if available
                new_child_value = list(child["values"])  # The new child's values
                if matching_reference:
                    formula_index = (
                        len(matching_reference["values"]) - 1
                    )  # Assuming formula is the last value
                    new_child_value[-1] = matching_reference["values"][formula_index]

                # Add placeholders for columns
                new_child_value.insert(0, "")
                new_child_value.insert(0, "")
                new_child_value.insert(0, "")
                child.update({"values": new_child_value})

            # Update the children of the derived item
            selected_GWMitem.update({"children": children})

        # Add the new GWM items to the appropriate location
        if isinstance(selected_node, list) and selected_GWMitems_copy:
            # Handle adding to list of strings (last level)
            parent_node["children"].extend(selected_GWMitems_copy)
        elif selected_node and "children" in selected_node and selected_GWMitems_copy:
            # Handle adding matched WMs to regular children
            selected_node["children"].extend(selected_GWMitems_copy)


class TreeDataManager_treesheet(TreeDataManager):
    def __init__(self, state, related_widget=None):
        super().__init__(state, related_widget=related_widget)
