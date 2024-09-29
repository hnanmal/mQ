# src/tabs/familyType_manage_tab/checkListbox.py
import tkinter as tk
from tkinter import ttk


class CheckListCanvas:
    def __init__(self, state, root):
        self.root = root

        # Variables and data structures

        self.items = [
            "Item 1",
        ]

        self.selected_items = []
        self.vars = []

        # Setup the layout
        self.setup_ui(state, self.items)

    def setup_ui(self, state, data):
        """Set up the UI components."""
        # Container for the checkboxes and labels
        try:
            self.canvas_frame.destroy()
        except:
            pass
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack()
        self.canvas_frame = canvas_frame

        # Canvas to hold checkboxes and labels
        self.canvas = tk.Canvas(canvas_frame, width=150, height=500)
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
        self.inner_frame = tk.Frame(self.canvas, width=200, relief="groove")
        self.canvas.create_window(
            (0, 20),
            window=self.inner_frame,
            anchor="nw",
        )

        # Create checkboxes and labels
        # self.create_checkboxes([])
        self.create_checkboxes(data)

        # Selected items listbox
        self.selected_listbox = tk.Listbox(
            canvas_frame, height=len(list(set(data))) + 3
        )
        self.selected_listbox.pack(pady=20)

    def create_checkboxes(self, data_):
        """Create checkboxes and labels for the list of items."""
        data = list(set(data_))
        for i, item in enumerate(data):
            var = tk.BooleanVar()
            self.vars.append(var)
            checkbox = tk.Checkbutton(
                self.inner_frame,
                variable=var,
                command=lambda item=item, var=var: self.on_check(item, var),
            )
            checkbox.grid(row=i * 2, column=0, sticky="w")
            label = ttk.Label(self.inner_frame, text=item)
            label.grid(row=i * 2 + 1, column=0, sticky="w")
        # self.inner_frame.columnconfigure(0, weight=0)
        # self.inner_frame.columnconfigure(1, weight=0)

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

    def set_data(self, state, data):
        self.items = data
        self.setup_ui(state, data)
