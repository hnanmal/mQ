class TreeDataManager:
    def __init__(self, state, related_widget=None):
        self.state = state
        self.team_std_info = state.team_std_info
        # self.data_kind = related_widget.data_kind  # 대비용(필요없으면 추후 삭제)

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

    def update_node_value(self, data_kind, selected_name, column_index, new_value):
        """Update the value of a node in the tree."""

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

        # Find the selected node
        selected_node = find_node_recursive(
            self.team_std_info[data_kind]["children"], selected_name
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
                f"Updated node value: {selected_name}, column {column_index} to {new_value}"
            )
        else:
            print(f"Could not find node '{selected_name}' or 'values' key is missing.")

    def update_node_name(self, data_kind, selected_name, new_name):
        """Update the name of a node in the tree."""

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

        # Find the selected node
        selected_node = find_node_recursive(
            self.team_std_info[data_kind]["children"], selected_name
        )

        if selected_node is not None:
            selected_node["name"] = new_name
            print(f"Updated node name: {selected_name} to {new_name}")
        else:
            print(f"Could not find node '{selected_name}' to update name.")

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

    def delete_node(self, data_kind, selected_name):
        """Delete the specified node from the tree."""
        try:
            # Try to find the parent node of the selected item
            def find_parent_node_recursive(data, target_name):
                if not isinstance(data, list):
                    return None, None
                for node in data:
                    if "children" in node:
                        # Check if the target node is in the children
                        for child in node["children"]:
                            if child["name"] == target_name:
                                return node, child
                        # Recur to find the parent in deeper levels
                        parent_node, child_node = find_parent_node_recursive(
                            node["children"], target_name
                        )
                        if parent_node:
                            return parent_node, child_node
                return None, None

            # Find the parent node and the selected node to delete
            parent_node, selected_node = find_parent_node_recursive(
                self.team_std_info[data_kind]["children"], selected_name
            )

            if parent_node and selected_node:
                # Remove the selected node from the parent's children
                parent_node["children"].remove(selected_node)
                print(f"Deleted node: {selected_name}")
            else:
                print(f"Could not find selected node '{selected_name}' or its parent.")
        except Exception as e:
            print(f"Error deleting node: {e}")

    ###### 특수 ######
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
        """Add specified matched WMs to the children of the selected node."""
        _, parent_node, selected_node = self.get_node_path(
            data_kind, grandparent_name, parent_name, child_name
        )

        for selected_GWMitem in selected_GWMitems:
            new_values = list(selected_GWMitem["values"])
            new_values.insert(0, "")
            new_values.insert(0, "")
            new_values.insert(0, "")
            selected_GWMitem.update({"values": new_values})

        if isinstance(selected_node, list) and selected_GWMitems:
            # Handle adding to list of strings (last level)
            print(f"Adding matched WMs: {selected_GWMitems}")
            parent_node["children"].extend(selected_GWMitems)
        elif selected_node and "children" in selected_node and selected_GWMitems:
            # Handle adding matched WMs to regular children
            print(f"Adding matched WMs: {selected_GWMitems}")
            selected_node["children"].extend(selected_GWMitems)
