import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tabbed Page App")
        self.geometry("1400x900")  # Window size

        # Track expand/collapse state
        self.is_expanded = True

        # Create a notebook (tabbed pane)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # List of tab names and top-level item names (without numbers and periods)
        tab_names = [
            "형식 표준 구성도", "계산 기준",
            "Room", "Floors", "Roofs", "Walls_Ext", "Walls_Int",
            "St_Fdn", "St_Col", "St_Framing", "Ceilings", "Doors",
            "Windows", "Stairs", "Railings", "Generic", "Manual_Input"
        ]
        self.top_level_items = tab_names[2:]  # Top-level items without numbers and periods

        # Create tabs with the specified names
        for i, name in enumerate(tab_names):
            if name == "형식 표준 구성도":
                self.create_single_area_tab(name)
            else:
                self.create_three_area_tab(name)

    def create_single_area_tab(self, name):
        # Create a frame for the tab
        tab_frame = ttk.Frame(self.notebook)
        tab_frame.pack(fill='both', expand=True)

        # Frame for buttons at the top
        button_frame = ttk.Frame(tab_frame)
        button_frame.pack(fill='x', padx=10, pady=10)

        # Buttons to add, remove items, save and load configuration
        add_button = ttk.Button(button_frame, text="Add Item", command=self.add_item)
        remove_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected_item)
        save_button = ttk.Button(button_frame, text="Save", command=self.save_configuration)
        load_button = ttk.Button(button_frame, text="Load", command=self.load_configuration)
        self.toggle_button = ttk.Button(button_frame, text="Collapse All", command=self.toggle_expand_collapse)

        # Pack buttons with less padding
        add_button.pack(side="left", padx=2, pady=5)
        remove_button.pack(side="left", padx=2, pady=5)
        save_button.pack(side="left", padx=2, pady=5)
        load_button.pack(side="left", padx=2, pady=5)
        self.toggle_button.pack(side="left", padx=2, pady=5)

        # Create and pack the Treeview widget inside this tab
        self.tree = ttk.Treeview(tab_frame, columns=("name", "description"), style="Custom.Treeview")
        self.tree.column("#0", width=50, minwidth=50, anchor="center")  # Number column
        self.tree.column("name", width=300, minwidth=200)
        self.tree.column("description", width=400, minwidth=200)
        self.tree.heading("#0", text="#")
        self.tree.heading("name", text="Item")
        self.tree.heading("description", text="Description")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Add initial top-level items to the tree
        for i, item in enumerate(self.top_level_items):
            self.add_numbered_item("", f"{i}", item, f"{item} description")

        # Add double-click event for editing item names
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Add the tab to the notebook
        self.notebook.add(tab_frame, text=f"   {name}   ")

    def create_three_area_tab(self, name):
        # Create a frame for the tab
        tab_frame = ttk.Frame(self.notebook)

        # Create left, middle, and right frames
        left_frame = ttk.Frame(tab_frame)
        middle_frame = ttk.Frame(tab_frame)
        right_frame = ttk.Frame(tab_frame)

        # Left content
        left_label = ttk.Label(left_frame, text=f"Left content of {name}")
        left_button = ttk.Button(left_frame, text="Left Button", command=lambda: self.on_button_click(f"Left Button on {name}"))
        left_text = tk.Text(left_frame, height=5, width=30)

        # Middle content
        middle_label = ttk.Label(middle_frame, text=f"Middle content of {name}")
        middle_button = ttk.Button(middle_frame, text="Middle Button", command=lambda: self.on_button_click(f"Middle Button on {name}"))
        middle_text = tk.Text(middle_frame, height=5, width=30)

        # Right content
        right_label = ttk.Label(right_frame, text=f"Right content of {name}")
        right_button = ttk.Button(right_frame, text="Right Button", command=lambda: self.on_button_click(f"Right Button on {name}"))
        right_text = tk.Text(right_frame, height=5, width=30)

        # Pack left content with padding
        left_label.pack(padx=20, pady=10)
        left_button.pack(padx=20, pady=10)
        left_text.pack(padx=20, pady=10)

        # Pack middle content with padding
        middle_label.pack(padx=20, pady=10)
        middle_button.pack(padx=20, pady=10)
        middle_text.pack(padx=20, pady=10)

        # Pack right content with padding
        right_label.pack(padx=20, pady=10)
        right_button.pack(padx=20, pady=10)
        right_text.pack(padx=20, pady=10)

        # Layout left, middle, and right frames
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        middle_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Add the tab to the notebook with increased padding
        self.notebook.add(tab_frame, text=f"   {name}   ")

    def add_numbered_item(self, parent, number, original_name, description):
        item_id = self.tree.insert(parent, "end", text=number, values=(original_name, description))
        self.update_displayed_name(item_id)
        return item_id

    def update_displayed_name(self, item):
        # Retrieve the original name
        original_name = self.tree.set(item, "name")
        # Indent the display name based on the item's depth
        depth = self.get_item_depth(item)
        indented_name = " " * (depth * 4) + original_name
        # Update the displayed name
        self.tree.set(item, "name", indented_name)

    def get_item_depth(self, item):
        depth = 0
        parent = self.tree.parent(item)
        while parent:
            depth += 1
            parent = self.tree.parent(parent)
        return depth

    def add_item(self):
        selected_item = self.tree.focus()
        if not selected_item:
            # Add a top-level item if no item is selected
            new_index = len(self.tree.get_children())
            new_item_id = self.add_numbered_item("", str(new_index), "New Top-level Item", "New top-level description")
            self.tree.selection_set(new_item_id)
        else:
            # Add a sub-item under the selected item
            parent_number = self.tree.item(selected_item, "text")
            children = self.tree.get_children(selected_item)
            new_index = len(children) + 1
            new_number = f"{parent_number}.{new_index}"
            new_item_id = self.add_numbered_item(selected_item, new_number, "New Sub-item", "New sub-item description")
            self.tree.selection_set(new_item_id)
            # Automatically expand the parent item to show the new sub-item
            self.tree.item(selected_item, open=True)

    def remove_selected_item(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return

        # Remove selected items and collect parent items for renumbering
        parents_to_renumber = set()
        for item in selected_items:
            parent = self.tree.parent(item)
            if parent:
                parents_to_renumber.add(parent)
            self.tree.delete(item)

        # Renumber the children of each parent item
        for parent in parents_to_renumber:
            self.renumber_children(parent)

    def renumber_children(self, parent):
        children = self.tree.get_children(parent)
        for i, child in enumerate(children, start=1):
            # Renumber child
            parent_number = self.tree.item(parent, "text")
            new_number = f"{parent_number}.{i}"
            self.tree.item(child, text=new_number)
            self.update_displayed_name(child)
            # Recursively renumber children's children
            self.renumber_children(child)

    def get_descendants(self, item):
        # Recursively collect all descendants of an item
        descendants = set()
        children = self.tree.get_children(item)
        for child in children:
            descendants.add(child)
            descendants.update(self.get_descendants(child))
        return descendants

    def on_item_double_click(self, event):
        selected_item = self.tree.focus()
        column = self.tree.identify_column(event.x)
        if column == "#1":  # Display name column
            original_name = self.tree.set(selected_item, "name")  # Get original name
            # Create an Entry widget to edit the item name
            entry = ttk.Entry(self.tree, width=len(original_name) + 5)
            entry.insert(0, original_name)
            entry.bind("<Return>", lambda e: self.on_item_edit(entry, selected_item, column))
            entry.bind("<FocusOut>", lambda e: self.on_item_edit(entry, selected_item, column))
            entry.place(x=event.x, y=event.y)
            entry.focus()

    def on_item_edit(self, entry, item, column):
        new_value = entry.get()
        description = self.tree.set(item, "description")  # Preserve description
        # Update the original name and redisplay
        self.tree.set(item, "name", new_value)
        self.tree.set(item, "description", description)
        self.update_displayed_name(item)
        entry.destroy()

    def on_button_click(self, message):
        print(message)
        messagebox.showinfo("Button Clicked", message)

    def save_configuration(self):
        tree_data = []
        for item in self.tree.get_children():
            tree_data.append(self.get_item_data(item))
        # Save to JSON file
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(tree_data, f, indent=4)

    def get_item_data(self, item):
        item_data = {
            "number": self.tree.item(item, "text"),
            "name": self.tree.set(item, "name"),  # Save the original name without indentation
            "description": self.tree.set(item, "description"),
            "children": [self.get_item_data(child) for child in self.tree.get_children(item)]
        }
        return item_data

    def load_configuration(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                tree_data = json.load(f)
            # Clear existing tree
            for item in self.tree.get_children():
                self.tree.delete(item)
            # Load new tree
            for item_data in tree_data:
                self.insert_item_data("", item_data)

    def insert_item_data(self, parent, item_data):
        new_item = self.tree.insert(parent, "end", text=item_data["number"], values=(item_data["name"], item_data["description"]))
        self.update_displayed_name(new_item)
        for child_data in item_data["children"]:
            self.insert_item_data(new_item, child_data)

    def toggle_expand_collapse(self):
        if self.is_expanded:
            self.collapse_all()
            self.toggle_button.config(text="Expand All")
        else:
            self.expand_all()
            self.toggle_button.config(text="Collapse All")
        self.is_expanded = not self.is_expanded

    def expand_all(self):
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            self._expand_recursive(item)

    def _expand_recursive(self, item):
        for child in self.tree.get_children(item):
            self.tree.item(child, open=True)
            self._expand_recursive(child)

    def collapse_all(self):
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
            self._collapse_recursive(item)

    def _collapse_recursive(self, item):
        for child in self.tree.get_children(item):
            self.tree.item(child, open=False)
            self._collapse_recursive(child)

if __name__ == "__main__":
    app = App()
    app.mainloop()
