# src/tabs/familyType_manage_tab/checkListbox.py
import tkinter as tk
from tkinter import ttk


class CheckListCanvas:
    def __init__(self, root):
        self.root = root

        # Variables and data structures

        self.items = [
            "Item 1",
        ]

        self.selected_items = []
        self.vars = []

        # Setup the layout
        self.setup_ui(self.items)

    def setup_ui(self, data):
        """Set up the UI components."""
        # Container for the checkboxes and labels
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack()

        # Canvas to hold checkboxes and labels
        self.canvas = tk.Canvas(canvas_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the canvas
        scrollbar = tk.Scrollbar(
            canvas_frame, orient="vertical", command=self.canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configure canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Frame inside the canvas to hold the widgets
        self.inner_frame = tk.Frame(self.canvas, relief="groove")
        self.canvas.create_window(
            (20, 20),
            window=self.inner_frame,
            anchor="nw",
        )

        # Create checkboxes and labels
        self.create_checkboxes(data)

        # Selected items listbox
        self.selected_listbox = tk.Listbox(canvas_frame, height=len(data))
        self.selected_listbox.pack(pady=20)

    def create_checkboxes(self, data):
        """Create checkboxes and labels for the list of items."""
        for i, item in enumerate(data):
            var = tk.BooleanVar()
            self.vars.append(var)
            checkbox = tk.Checkbutton(
                self.inner_frame,
                variable=var,
                command=lambda item=item, var=var: self.on_check(item, var),
            )
            checkbox.grid(row=i, column=0, sticky="w")
            label = ttk.Label(self.inner_frame, text=item)
            label.grid(row=i, column=1, sticky="w")

    def on_check(self, item, var):
        """Handle checkbox and list item selection."""
        if var.get():
            self.selected_items.append(item)
        else:
            self.selected_items.remove(item)
        self.update_selected_list()

    def update_selected_list(self):
        """Update the listbox with selected items."""
        self.selected_listbox.delete(0, tk.END)
        for item in self.selected_items:
            self.selected_listbox.insert(tk.END, item)

    def set_data(self, data):
        self.items = data
        self.setup_ui(data)
