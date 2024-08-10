# Version: v1.4.4 (dragTrial)
# Changes:
# - Corrected the Alt key function to temporarily enable Order Adjustment Mode when dragging.

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox, simpledialog, font, Menu
import json
import pyperclip


class ColumnSelectionDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Select Column")
        ttk.Label(master, text="Paste into which column?").pack()
        self.selection = tk.StringVar(value="Item")
        ttk.Radiobutton(
            master, text="Item", variable=self.selection, value="Item"
        ).pack(anchor="w")
        ttk.Radiobutton(
            master, text="Description", variable=self.selection, value="Description"
        ).pack(anchor="w")
        return None

    def apply(self):
        self.result = self.selection.get()

### for app.py
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Tabbed Page App")    ### || for app.py > App class
        self.geometry("1400x900")  # Window size    ### || for app.py > App class

        # Create a dictionary to store original names
        self.original_names = {}    ### || for app.py > App class

        # Track the previous level limit
        self.previous_level_limit = 3  # Default level limit    ### || for app.py > App class

        # Create a notebook (tabbed pane)
        self.notebook = ttk.Notebook(self)    ### || for app.py > App class
        self.notebook.pack(fill="both", expand=True)    ### || for app.py > App class

        # List of tab names and top-level item names (without numbers and periods)
            ### || for app.py > App class
        tab_names = [
            "형식 표준 구성도",
            "계산 기준",
            "Room",
            "Floors",
            "Roofs",
            "Walls_Ext",
            "Walls_Int",
            "St_Fdn",
            "St_Col",
            "St_Framing",
            "Ceilings",
            "Doors",
            "Windows",
            "Stairs",
            "Railings",
            "Generic",
            "Manual_Input",
        ]
            ### || for app.py > App class
        self.top_level_items = tab_names[
            2:
        ]  # Top-level items without numbers and periods

            ### || for app.py > App class > 
        # Create tabs with the specified names
        for i, name in enumerate(tab_names):
            if name == "형식 표준 구성도":
                self.create_single_area_tab(name)
            else:
                self.create_three_area_tab(name)

            ### || for .py > SearchManager class > search_items method
        # Initialize search index
        self.search_results = []
        self.search_index = 0
        self.last_search_term = ""

            ### || for clipboard.py > ClipboardManager class > copy_to_clipboard method
        # Initialize copied item storage
        self.copied_items = []

            ### || for clipboard.py > ClipboardManager class > copy_to_clipboard method
        # Bind copy and paste shortcuts for external clipboard
        self.bind_all("<Control-c>", self.copy_to_clipboard)
        self.bind_all("<Control-v>", self.paste_from_clipboard)

        # Initialize right-click context menu
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Initialize drag-and-drop variables
        self.drag_data = {"x": 0, "y": 0, "items": []}

        # Add "Order Adjustment Mode" button
        self.order_adjustment_mode = tk.BooleanVar(value=False)
        self.order_adjustment_button = ttk.Button(
            self,
            text="Order Adjustment Mode: OFF",
            command=self.toggle_order_adjustment_mode,
        )
        self.order_adjustment_button.pack(side="top", anchor="w", padx=10, pady=5)

        # Track whether the item is in text editing mode
        self.is_text_editing = False

        # Bind Alt key for temporary Order Adjustment Mode
        self.bind_all("<Alt-KeyPress>", self.alt_key_pressed)
        self.bind_all("<Alt-KeyRelease>", self.alt_key_released)

        # Track if Alt key is held down
        self.alt_key_down = False

    def alt_key_pressed(self, event):
        self.alt_key_down = True

    def alt_key_released(self, event):
        self.alt_key_down = False

    def toggle_order_adjustment_mode(self):
        self.order_adjustment_mode.set(not self.order_adjustment_mode.get())
        mode_text = "ON" if self.order_adjustment_mode.get() else "OFF"
        self.order_adjustment_button.config(text=f"Order Adjustment Mode: {mode_text}")
        # Only enable drag-and-drop bindings when order adjustment mode is ON
        if self.order_adjustment_mode.get():
            self.tree.bind("<ButtonPress-1>", self.on_drag_start)
            self.tree.bind("<B1-Motion>", self.on_drag_motion)
            self.tree.bind("<ButtonRelease-1>", self.on_drag_release)
        else:
            self.tree.unbind("<ButtonPress-1>")
            self.tree.unbind("<B1-Motion>")
            self.tree.unbind("<ButtonRelease-1>")

    def create_single_area_tab(self, name):
        # Create a frame for the tab
        tab_frame = ttk.Frame(self.notebook)
        tab_frame.pack(fill="both", expand=True)

        # Frame for buttons at the top
        button_frame = ttk.Frame(tab_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Buttons to add, remove items, save and load configuration
        add_button = ttk.Button(button_frame, text="Add Item", command=self.add_item)
        remove_button = ttk.Button(
            button_frame, text="Remove Selected", command=self.remove_selected_item
        )
        save_button = ttk.Button(
            button_frame, text="Save", command=self.save_configuration
        )
        load_button = ttk.Button(
            button_frame, text="Load", command=self.load_configuration
        )
        collapse_button = ttk.Button(
            button_frame, text="Collapse All", command=self.collapse_all
        )

        # Level limit combobox
        self.level_limit_var = tk.StringVar()
        self.level_limit_combo = ttk.Combobox(
            button_frame, textvariable=self.level_limit_var, state="readonly", width=10
        )
        self.level_limit_combo["values"] = [
            str(i) for i in range(1, 11)
        ]  # Levels 1 to 10
        self.level_limit_combo.current(2)  # Default to level 3
        self.level_limit_combo.bind("<<ComboboxSelected>>", self.update_level_limit)

        # Search entry and button
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(button_frame, textvariable=self.search_var, width=30)
        search_entry.bind("<Return>", self.on_enter_key)
        search_button = ttk.Button(
            button_frame, text="Search", command=self.search_items
        )

        # Pack buttons and combobox
        add_button.pack(side="left", padx=2, pady=5)
        remove_button.pack(side="left", padx=2, pady=5)
        save_button.pack(side="left", padx=2, pady=5)
        load_button.pack(side="left", padx=2, pady=5)
        collapse_button.pack(side="left", padx=2, pady=5)
        self.level_limit_combo.pack(side="left", padx=2, pady=5)
        search_entry.pack(side="right", padx=2, pady=5)
        search_button.pack(side="right", padx=2, pady=5)

        # Create a frame for the treeview and scrollbar
        tree_frame = ttk.Frame(tab_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a vertical scrollbar and associate it with the treeview
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")

        # Create a style for the Treeview to ensure custom tag colors are applied
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.map(
            "Treeview",
            background=[("selected", "blue")],
            foreground=[("selected", "white")],
        )

        # Create and pack the Treeview widget inside this frame
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("indented_name", "description"),
            show="tree headings",
            yscrollcommand=tree_scroll.set,
            style="Treeview",
        )
        self.tree.column("#0", width=50, anchor="center")  # Tree structure column
        self.tree.column("indented_name", width=300, minwidth=200)
        self.tree.column("description", width=400, minwidth=200)
        self.tree.heading("#0", text="#")
        self.tree.heading("indented_name", text="Item")
        self.tree.heading("description", text="Description")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Configure the scrollbar
        tree_scroll.config(command=self.tree.yview)

        # Define custom fonts
        self.font_level_0 = font.Font(family="Arial", size=12)
        self.font_level_4 = font.Font(family="Arial", size=10)
        self.default_font = font.Font(family="Arial", size=10)  # Default font size

        # Define tag for top-level items with light green background and bold font
        self.tree.tag_configure(
            "top_level", background="light green", font=self.font_level_0
        )
        # Define tag for level 4 items with blue foreground and custom font
        self.tree.tag_configure("level_4", foreground="blue", font=self.font_level_4)

        # Add initial top-level items to the tree
        for i, item in enumerate(self.top_level_items):
            self.add_numbered_item("", f"{i}", item, "", top_level=True)

        # Bind double-click event for editing item names
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Add single-click event for editing descriptions
        self.tree.bind("<Button-1>", self.on_item_single_click)

        # Bind mouse events for drag-and-drop functionality
        self.tree.bind("<ButtonPress-1>", self.on_drag_start)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_release)

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
        left_button = ttk.Button(
            left_frame,
            text="Left Button",
            command=lambda: self.on_button_click(f"Left Button on {name}"),
        )
        left_text = tk.Text(left_frame, height=5, width=30)

        # Middle content
        middle_label = ttk.Label(middle_frame, text=f"Middle content of {name}")
        middle_button = ttk.Button(
            middle_frame,
            text="Middle Button",
            command=lambda: self.on_button_click(f"Middle Button on {name}"),
        )
        middle_text = tk.Text(middle_frame, height=5, width=30)

        # Right content
        right_label = ttk.Label(right_frame, text=f"Right content of {name}")
        right_button = ttk.Button(
            right_frame,
            text="Right Button",
            command=lambda: self.on_button_click(f"Right Button on {name}"),
        )
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

    def add_numbered_item(
        self, parent, number, original_name, description, top_level=False
    ):
        depth = self.get_item_depth(parent) + 1
        tags = ("top_level",) if top_level else ()
        if depth == 4:
            tags = ("level_4",)
        item_id = self.tree.insert(
            parent, "end", text=number, values=(original_name, description), tags=tags
        )
        self.original_names[item_id] = original_name  # Store original name internally
        self.update_displayed_name(item_id)
        return item_id

    def update_displayed_name(self, item):
        # Retrieve the original name from the internal storage
        original_name = self.original_names.get(item, "")
        # Indent the display name based on the item's depth
        depth = self.get_item_depth(item)
        indented_name = " " * (depth * 4) + original_name
        # Update the displayed name in the tree
        self.tree.set(item, "indented_name", indented_name)

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
            new_item_id = self.add_numbered_item(
                "", str(new_index), "New Top-level Item", "", top_level=True
            )
            self.tree.selection_set(new_item_id)
        else:
            # Add a sub-item under the selected item
            parent_number = self.tree.item(selected_item, "text")
            children = self.tree.get_children(selected_item)
            new_index = len(children) + 1
            new_number = f"{parent_number}.{new_index}"
            new_item_id = self.add_numbered_item(
                selected_item, new_number, "New Sub-item", ""
            )
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
            # Remove the original name from the internal storage
            self.original_names.pop(item, None)

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

    def on_item_single_click(self, event):
        selected_item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        # Check if the Description column (index #2) is clicked
        if column == "#2":  # "#2" corresponds to the Description column
            self.edit_description(selected_item)

    def on_item_double_click(self, event):
        # Get the selected item and the column clicked
        selected_item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        # Check if the Item column (index #1) is clicked
        if column == "#1":
            self.edit_item_name(selected_item)

    def edit_item_name(self, item):
        # Get current item name value
        current_value = self.original_names.get(item, "")

        # Set editing mode flag
        self.is_text_editing = True

        # Create an Entry widget to edit the item name
        entry = ttk.Entry(self.tree, width=len(current_value) + 5)
        entry.insert(0, current_value)
        entry.bind("<Return>", lambda e: self.save_item_name(entry, item))
        entry.bind("<FocusOut>", lambda e: self.save_item_name(entry, item))
        bbox = self.tree.bbox(item, column="indented_name")
        if bbox:
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
            entry.focus()
        else:
            # If bbox is not available, destroy the entry to avoid orphan widgets
            entry.destroy()

    def save_item_name(self, entry, item):
        try:
            new_value = entry.get()
            self.original_names[item] = new_value  # Update the original name
            self.update_displayed_name(item)  # Update displayed name with the new value
        except tk.TclError:
            # This error can occur if the entry is destroyed before this method is called
            pass
        finally:
            self.is_text_editing = False  # Clear editing mode flag
            entry.destroy()

    def edit_description(self, item):
        # Get current description value
        current_value = self.tree.set(item, "description")

        # Set editing mode flag
        self.is_text_editing = True

        # Create an Entry widget to edit the description
        entry = ttk.Entry(self.tree, width=len(current_value) + 5)
        entry.insert(0, current_value)
        entry.bind("<Return>", lambda e: self.save_description(entry, item))
        entry.bind("<FocusOut>", lambda e: self.save_description(entry, item))
        bbox = self.tree.bbox(item, column="description")
        if bbox:
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
            entry.focus()
        else:
            # If bbox is not available, destroy the entry to avoid orphan widgets
            entry.destroy()

    def save_description(self, entry, item):
        try:
            new_value = entry.get()
            self.tree.set(item, "description", new_value)
        except tk.TclError:
            # This error can occur if the entry is destroyed before this method is called
            pass
        finally:
            self.is_text_editing = False  # Clear editing mode flag
            entry.destroy()

    def on_button_click(self, message):
        print(message)
        messagebox.showinfo("Button Clicked", message)

    def save_configuration(self):
        tree_data = []
        for item in self.tree.get_children():
            tree_data.append(self.get_item_data(item))
        # Save to JSON file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(tree_data, f, indent=4, ensure_ascii=False)

    def get_item_data(self, item):
        item_data = {
            "number": self.tree.item(item, "text"),
            "name": self.original_names.get(
                item, ""
            ),  # Retrieve the original name from storage
            "description": self.tree.set(item, "description"),
            "children": [
                self.get_item_data(child) for child in self.tree.get_children(item)
            ],
        }
        return item_data

    def load_configuration(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                tree_data = json.load(f)
            # Clear existing tree
            for item in self.tree.get_children():
                self.tree.delete(item)
            # Load new tree
            for item_data in tree_data:
                self.insert_item_data("", item_data)

    def insert_item_data(self, parent, item_data):
        depth = self.get_item_depth(parent) + 1
        tags = ("top_level",) if parent == "" else ()
        if depth == 4:
            tags = ("level_4",)
        new_item = self.tree.insert(
            parent,
            "end",
            text=item_data["number"],
            values=(item_data["name"], item_data["description"]),
            tags=tags,
        )
        self.original_names[new_item] = item_data[
            "name"
        ]  # Store original name internally
        self.update_displayed_name(new_item)
        for child_data in item_data["children"]:
            self.insert_item_data(new_item, child_data)

    def collapse_all(self):
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
            self._collapse_recursive(item)

    def _collapse_recursive(self, item):
        for child in self.tree.get_children(item):
            self.tree.item(child, open=False)
            self._collapse_recursive(child)

    def update_level_limit(self, event):
        # Get the selected level limit
        new_level_limit = int(self.level_limit_var.get())

        # Collapse nodes below the previous level limit
        if new_level_limit < self.previous_level_limit:
            self.collapse_all_to_level(new_level_limit)

        # Expand the tree based on the selected level limit
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            self._expand_recursive(item, current_level=1, level_limit=new_level_limit)

        # Update the previous level limit
        self.previous_level_limit = new_level_limit

    def collapse_all_to_level(self, level_limit):
        for item in self.tree.get_children():
            self._collapse_to_level_recursive(
                item, current_level=1, level_limit=level_limit
            )

    def _collapse_to_level_recursive(self, item, current_level, level_limit):
        if current_level >= level_limit:
            for child in self.tree.get_children(item):
                self.tree.item(child, open=False)
        else:
            for child in self.tree.get_children(item):
                self._collapse_to_level_recursive(
                    child, current_level=current_level + 1, level_limit=level_limit
                )

    def _expand_recursive(self, item, current_level, level_limit):
        if current_level >= level_limit:
            return
        for child in self.tree.get_children(item):
            self.tree.item(child, open=True)
            self._expand_recursive(
                child, current_level=current_level + 1, level_limit=level_limit
            )

    def search_items(self):
        search_term = self.search_var.get().lower()
        if not search_term:
            return

        # Get all items in the treeview
        items = self.tree.get_children("")
        self.search_results = []

        def recursive_search(item):
            if search_term in self.tree.item(item, "values")[0].lower():
                self.search_results.append(item)
            for child in self.tree.get_children(item):
                recursive_search(child)

        for item in items:
            recursive_search(item)

        if self.search_results:
            self.search_index = 0
            self.select_search_result()

    def select_search_result(self):
        if self.search_results:
            item = self.search_results[self.search_index]
            self.tree.selection_set(item)
            self.tree.see(item)
            self.search_index = (self.search_index + 1) % len(self.search_results)

    def on_enter_key(self, event):
        search_term = self.search_var.get().lower()
        if search_term != self.last_search_term:
            self.search_results = []
            self.search_index = 0
            self.last_search_term = search_term

        if not self.search_results:
            self.search_items()
        else:
            self.select_search_result()

    def copy_to_clipboard(self, event=None):
        if self.is_text_editing:
            return  # Skip clipboard operation if in text editing mode
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an item to copy.")
            return
        clipboard_data = "\n".join(
            [self.original_names[item] for item in selected_items]
        )
        pyperclip.copy(clipboard_data)
        messagebox.showinfo("Copy", "Selected items copied to clipboard.")

    def paste_from_clipboard(self, event=None):
        if self.is_text_editing:
            # Directly paste clipboard content into the focused entry widget
            clipboard_text = pyperclip.paste()
            entry = self.focus_get()
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)  # Clear the current content
                entry.insert(tk.END, clipboard_text)  # Insert clipboard content
            return

        clipboard_text = pyperclip.paste()
        selected_items = self.tree.selection()

        # If clipboard contains tab-separated values and matches the number of selected items
        if clipboard_text and selected_items:
            clipboard_lines = clipboard_text.split("\n")
            clipboard_lines = [
                line for line in clipboard_lines if line
            ]  # Remove empty lines
            if len(clipboard_lines) == len(selected_items):
                target_column = (
                    self.ask_target_column()
                )  # Ask the user for target column
                if target_column is None:
                    return  # If user cancels the operation
                for item, text in zip(selected_items, clipboard_lines):
                    if target_column == "Item":
                        self.original_names[item] = text  # Update the original name
                        self.update_displayed_name(
                            item
                        )  # Update displayed name with the new value
                    elif target_column == "Description":
                        self.tree.set(
                            item, "description", text
                        )  # Update the description
                return

    def ask_target_column(self):
        dialog = ColumnSelectionDialog(self)
        return dialog.result

    def paste_item_data(self, parent, item_data):
        parent_number = self.tree.item(parent, "text")
        children = self.tree.get_children(parent)
        new_index = len(children) + 1
        new_number = f"{parent_number}.{new_index}"
        new_item = self.tree.insert(
            parent,
            "end",
            text=new_number,
            values=(item_data["name"], item_data["description"]),
        )
        self.original_names[new_item] = item_data["name"]
        self.update_displayed_name(new_item)
        for child_data in item_data["children"]:
            self.paste_item_data(new_item, child_data)

    def show_context_menu(self, event):
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="Copy", command=self.copy_selected_items)
        context_menu.add_command(label="Paste", command=self.paste_copied_items)
        context_menu.add_separator()
        context_menu.add_command(
            label="상위레벨로", command=self.move_items_up_one_level
        )
        context_menu.add_command(
            label="하위레벨로", command=self.move_items_down_one_level
        )
        context_menu.post(event.x_root, event.y_root)

    def copy_selected_items(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an item to copy.")
            return
        self.copied_items = [self.get_item_data(item) for item in selected_items]
        messagebox.showinfo("Copy", "Selected items copied successfully.")

    def paste_copied_items(self):
        if not self.copied_items:
            messagebox.showwarning("No Copy", "No copied items to paste.")
            return
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "No Selection", "Please select an item to paste into."
            )
            return
        for item_data in self.copied_items:
            self.paste_item_data(selected_items[0], item_data)
        messagebox.showinfo("Paste", "Copied items pasted successfully.")
        self.copied_items = []  # Clear copied items after pasting
        self.tree.item(selected_items[0], open=True)

    def on_drag_start(self, event):
        if not self.order_adjustment_mode.get() and not self.alt_key_down:
            return
        items = self.tree.selection()
        if items:
            self.drag_data["items"] = items
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        if not self.order_adjustment_mode.get() and not self.alt_key_down:
            return
        if self.drag_data["items"]:
            for item in self.drag_data["items"]:
                self.tree.selection_set(item)
            self.tree.focus(self.drag_data["items"][0])

    def on_drag_release(self, event):
        if not self.order_adjustment_mode.get() and not self.alt_key_down:
            return
        if not self.drag_data["items"]:
            return

        target_item = self.tree.identify_row(event.y)
        if not target_item or target_item in self.drag_data["items"]:
            self.drag_data = {"x": 0, "y": 0, "items": []}
            return

        if messagebox.askyesno(
            "Confirm Move", "Do you want to move the selected items here?"
        ):
            self.move_items(self.drag_data["items"], target_item)

        # Ensure all UI updates are complete before removing selection
        self.update_idletasks()

        # Clear the selection after moving
        self.tree.selection_remove(self.tree.selection())
        self.drag_data = {"x": 0, "y": 0, "items": []}

    def move_items(self, items, target_item):
        target_parent = self.tree.parent(target_item)
        target_index = self.tree.index(target_item)

        for item in items:
            parent = self.tree.parent(item)
            if parent == target_parent:
                # Same level move within the same parent
                self.tree.move(item, target_parent, target_index)
            else:
                # Move to a different level
                if self.get_item_depth(item) == self.get_item_depth(target_item):
                    self.tree.move(item, target_parent, target_index)
                else:
                    # Move to the end of the target parent
                    self.tree.move(item, target_item, "end")

            self.renumber_children(parent)
        self.renumber_children(target_parent)

    def move_items_up_one_level(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            parent = self.tree.parent(item)
            if parent:
                grandparent = self.tree.parent(parent)
                if grandparent:
                    self.tree.move(item, grandparent, self.tree.index(parent) + 1)
                    self.renumber_children(grandparent)
        messagebox.showinfo("Level Change", "Selected items moved up one level.")

    def move_items_down_one_level(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            previous_sibling = self.tree.prev(item)
            if previous_sibling:
                self.tree.move(item, previous_sibling, "end")
                self.renumber_children(previous_sibling)
        messagebox.showinfo("Level Change", "Selected items moved down one level.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
