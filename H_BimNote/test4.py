import tkinter as tk
from tkinter import ttk


class AlternatingRowColorTreeViewApp:
    def __init__(self, root):
        # Set up the main frame
        self.root = root
        self.root.title("Alternating Row Colors in TreeView")

        # Create the TreeView widget
        self.tree = ttk.Treeview(root, columns=("Value1", "Value2"), show="headings")
        self.tree.heading("Value1", text="Column 1")
        self.tree.heading("Value2", text="Column 2")

        # Add the TreeView widget to the window
        self.tree.pack(expand=True, fill="both")

        # Add some sample data
        self.add_data()

        # Apply alternate row colors
        self.apply_alternate_row_colors()

    def add_data(self):
        # Adding data to TreeView
        sample_data = [
            ("Row 1, Value 1", "Row 1, Value 2"),
            ("Row 2, Value 1", "Row 2, Value 2"),
            ("Row 3, Value 1", "Row 3, Value 2"),
            ("Row 4, Value 1", "Row 4, Value 2"),
            ("Row 5, Value 1", "Row 5, Value 2"),
        ]
        for item in sample_data:
            self.tree.insert("", "end", values=item)

    def apply_alternate_row_colors(self):
        """Apply alternate row colors to the Treeview."""
        for i, item in enumerate(self.tree.get_children("")):
            # Alternate between two different tags: evenrow and oddrow
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.item(item, tags=(tag,))

        # Configure the styles for the tags
        self.tree.tag_configure("evenrow", background="white")
        self.tree.tag_configure("oddrow", background="lightgray")


if __name__ == "__main__":
    root = tk.Tk()
    app = AlternatingRowColorTreeViewApp(root)
    root.mainloop()
