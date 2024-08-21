import tkinter as tk
from tkinter import ttk


class TestApp:
    def __init__(self, root):
        self.tree = ttk.Treeview(root, columns=("Item", "Description"))
        self.tree.heading("#0", text="Number")
        self.tree.heading("#1", text="Item")
        self.tree.heading("#2", text="Description")
        self.tree.pack(expand=True, fill="both")

        self.original_names = {}
        self.add_test_items()

    def get_item_depth(self, item):
        depth = 0
        parent = self.tree.parent(item)
        while parent:
            depth += 1
            parent = self.tree.parent(parent)
        return depth

    def update_displayed_name(self, item):
        original_name = self.original_names.get(item, "")
        depth = self.get_item_depth(item)
        indented_name = " " * (depth * 4) + original_name
        print(f"Item: {item}, Depth: {depth}, Indented Name: '{indented_name}'")
        self.tree.set(item, "Item", indented_name)

    def add_test_items(self):
        parent = ""
        for i in range(5):
            item_id = self.tree.insert(
                parent, "end", text=f"item_{i}", values=(f"Item {i}", "")
            )
            self.original_names[item_id] = f"Item {i}"
            self.update_displayed_name(item_id)
            parent = item_id  # Set the new item as the parent for the next one


if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
