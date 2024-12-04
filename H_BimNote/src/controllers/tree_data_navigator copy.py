class TreeDataManager:
    def __init__(self, state, related_widget=None):
        self.state = state
        self.team_std_info = state.team_std_info
        self.data_kind = related_widget.data_kind  # 대비용(필요없으면 추후 삭제)
        self.find_node_by_name_recur

    def register_related_widget(self, related_widget):
        self.related_widget = related_widget

    def find_node_by_name(self, data, target_name):
        """Find a node by its name in the given children list."""
        return next((node for node in data if node["name"] == target_name), None)

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

        # Navigate to the selected child node
        child_node = self.find_node_by_name(parent_node["children"], child_name)
        return grandparent_node, parent_node, child_node

    def remove_matched_wms(
        self, data_kind, grandparent_name, parent_name, child_name, matched_wms
    ):
        """Remove specified matched WMs from the children of the selected node."""
        _, _, selected_node = self.get_node_path(
            data_kind, grandparent_name, parent_name, child_name
        )

        if selected_node and "children" in selected_node:
            print(f"Removing matched WMs: {matched_wms}")
            selected_node["children"] = [
                child for child in selected_node["children"] if child not in matched_wms
            ]

    # def add_child_node(self, data_kind, grandparent_name, parent_name, new_child):
    #     """Add a new child node to the specified parent node."""
    #     _, parent_node, _ = self.get_node_path(
    #         data_kind, grandparent_name, parent_name, None
    #     )

    #     if parent_node and "children" in parent_node:
    #         parent_node["children"].append(new_child)

    def add_child_node(self, data_kind, selected_name, new_child_name):
        """Add a new child node to the specified selected node."""
        _, _, selected_node = self.get_node_path(data_kind, None, None, selected_name)

        if selected_node and "children" in selected_node:
            # Ensure the new child node has the correct structure
            new_child = {"name": new_child_name, "values": [], "children": []}
            selected_node["children"].append(new_child)

    def match_wms_to_stdType(
        self, data_kind, grandparent_name, parent_name, child_name, selected_wms
    ):
        """Add specified matched WMs to the children of the selected node."""
        _, _, selected_node = self.get_node_path(
            data_kind, grandparent_name, parent_name, child_name
        )

        if selected_node and "children" in selected_node and selected_wms:
            print(f"Adding matched WMs: {selected_wms}")
            selected_node["children"].extend(selected_wms)
            # 상태가 업데이트되었을 때 모든 관찰자에게 알림을 보냄
            self.state.observer_manager.notify_observers(self.state)
