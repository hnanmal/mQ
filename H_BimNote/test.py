import tkinter as tk
from tkinter import ttk


class BaseTreeView:
    def __init__(self, parent, headers):
        self.tree = ttk.Treeview(parent, columns=headers, show="headings")
        self.setup_columns(headers)
        self.tree.pack(expand=True, fill="both")

    def setup_columns(self, headers):
        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=100)

    def insert_data(self, parent, data):
        """Insert data recursively into Treeview."""
        for row in data:
            parent_id = self.tree.insert(parent, "end", values=(row["name"],))
            if "children" in row:
                self.insert_data(parent_id, row["children"])

    def clear_treeview(self):
        self.tree.delete(*self.tree.get_children())

    def get_item_indices(self, selected_item_id):
        indices = []
        current_item = selected_item_id
        while current_item:
            parent_id = self.tree.parent(current_item)
            siblings = self.tree.get_children(parent_id)
            item_index = siblings.index(current_item)
            if parent_id:
                parent_siblings = self.tree.get_children(self.tree.parent(parent_id))
                parent_index = parent_siblings.index(parent_id)
            else:
                parent_index = -1
            indices.insert(0, (parent_index, item_index))
            current_item = parent_id
        return indices

    def select_item_by_indices(self, indices):
        current_parent = ""
        target_item = None
        for parent_index, item_index in indices:
            children = self.tree.get_children(current_parent)
            if item_index < len(children):
                target_item = children[item_index]
                current_parent = target_item
            else:
                print(f"Index {item_index} is out of bounds for the current parent.")
                return
        if target_item:
            self.tree.selection_set(target_item)
            self.tree.focus(target_item)
            self.tree.see(target_item)


# Test code to verify the functionality
def test_treeview():
    # Setup tkinter root window
    root = tk.Tk()
    root.geometry("400x400")
    root.title("TreeView Test")

    # Create a TreeView widget
    headers = ["Item"]
    tree_view = BaseTreeView(root, headers)

    # Insert nested data into the TreeView
    initial_data = [
        {
            "name": "Root1",
            "children": [
                {"name": "Child1.1"},
                {
                    "name": "Child1.2",
                    "children": [
                        {"name": "Grandchild1.2.1"},
                        {"name": "Grandchild1.2.2"},
                    ],
                },
            ],
        },
        {
            "name": "Root2",
            "children": [
                {"name": "Child2.1"},
                {"name": "Child2.2", "children": [{"name": "Grandchild2.2.1"}]},
            ],
        },
    ]
    tree_view.insert_data("", initial_data)

    # Select a specific item (Grandchild1.2.1)
    grandchild_id = tree_view.tree.get_children()[0]  # Root1
    grandchild_id = tree_view.tree.get_children(grandchild_id)[1]  # Child1.2
    grandchild_id = tree_view.tree.get_children(grandchild_id)[0]  # Grandchild1.2.1

    tree_view.tree.selection_set(grandchild_id)
    tree_view.tree.focus(grandchild_id)

    # Get and print item indices
    indices = tree_view.get_item_indices(grandchild_id)
    print(f"Stored indices: {indices}")

    # Clear the TreeView
    tree_view.clear_treeview()

    # Re-insert the same data
    tree_view.insert_data("", initial_data)

    # Re-select the item using the stored indices
    tree_view.select_item_by_indices(indices)

    root.mainloop()


# Run the test
if __name__ == "__main__":
    test_treeview()
