# Version: 1.0.0
import tkinter as tk
from tkinter import simpledialog, ttk
from dialogs import ColumnSelectionDialog
import pyperclip


class ClipboardManager:
    def __init__(self, app):
        self.app = app
        self.app.copied_items = []  ### mk
        self.app.bind_all("<Control-c>", self.copy_to_clipboard)
        self.app.bind_all("<Control-v>", self.paste_from_clipboard)

    def get_item_data(self, item):
        item_data = {
            "number": self.app.tree.item(item, "text"),
            "name": self.app.original_names.get(
                item, ""
            ),  # Retrieve the original name from storage
            "description": self.app.tree.set(item, "description"),
            "children": [
                self.get_item_data(child) for child in self.app.tree.get_children(item)
            ],
        }
        return item_data

    def copy_to_clipboard(self, event=None):
        # self.app.copied_items = []  ### mk
        # self.app.bind_all("<Control-c>", self.copy_to_clipboard)
        # self.app.bind_all("<Control-v>", self.paste_from_clipboard)

        if self.app.is_text_editing:
            return  # Skip clipboard operation if in text editing mode
        selected_items = self.app.tree.selection()
        if not selected_items:
            tk.messagebox.showwarning("No Selection", "Please select an item to copy.")
            return
        clipboard_data = "\n".join(
            [self.app.original_names[item] for item in selected_items]
        )
        pyperclip.copy(clipboard_data)
        tk.messagebox.showinfo("Copy", "Selected items copied to clipboard.")

    def paste_from_clipboard(self, event=None):
        if self.app.is_text_editing:
            # Directly paste clipboard content into the focused entry widget
            clipboard_text = pyperclip.paste()
            entry = self.app.focus_get()
            if isinstance(entry, ttk.Entry):
                entry.delete(0, self.app.tk.END)  # Clear the current content
                entry.insert(
                    self.app.tk.END, clipboard_text
                )  # Insert clipboard content
            return

        clipboard_text = pyperclip.paste()
        selected_items = self.app.tree.selection()

        # If clipboard contains tab-separated values and matches the number of selected items
        if clipboard_text and selected_items:
            clipboard_lines = clipboard_text.split("\n")
            clipboard_lines = [
                line for line in clipboard_lines if line
            ]  # Remove empty lines
            if len(clipboard_lines) == len(selected_items):
                target_column = (
                    self.app.config_manager.ask_target_column()
                )  # Ask the user for target column
                if target_column is None:
                    return  # If user cancels the operation
                for item, text in zip(selected_items, clipboard_lines):
                    if target_column == "Item":
                        self.app.original_names[item] = text  # Update the original name
                        self.app.treeview_operations.update_displayed_name(
                            item
                        )  # Update displayed name with the new value
                    elif target_column == "Description":
                        self.app.tree.set(
                            item, "description", text
                        )  # Update the description
                return

    # def ask_target_column(self):
    #     dialog = ColumnSelectionDialog(self.app)
    #     return dialog.result

    def paste_item_data(self, parent, item_data):
        parent_number = self.app.tree.item(parent, "text")
        children = self.app.tree.get_children(parent)
        new_index = len(children) + 1
        new_number = f"{parent_number}.{new_index}"
        new_item = self.app.tree.insert(
            parent,
            "end",
            text=new_number,
            values=(item_data["name"], item_data["description"]),
        )
        self.app.original_names[new_item] = item_data["name"]
        self.app.treeview_operations.update_displayed_name(new_item)

        # Recursively paste children
        for child_data in item_data["children"]:
            self.paste_item_data(new_item, child_data)

        return new_item  # Return the newly created item
    
    def copy_selected_items(self):
        selected_items = self.app.tree.selection()
        if not selected_items:
            tk.messagebox.showwarning("No Selection", "Please select an item to copy.")
            return
        self.app.copied_items = [self.get_item_data(item) for item in selected_items]
        # tk.messagebox.showinfo("Copy", "Selected items copied successfully.")

    def paste_copied_items(self):
        if not self.app.copied_items:
            tk.messagebox.showwarning("No Copy", "No copied items to paste.")
            return
        selected_items = self.app.tree.selection()
        if not selected_items:
            tk.messagebox.showwarning(
                "No Selection", "Please select an item to paste into."
            )
            return
        
        pasted_items = []  # Track all pasted items for undo purposes
        # for item_data in self.app.copied_items:
        #     self.paste_item_data(selected_items[0], item_data)
        for item_data in self.app.copied_items:
            new_item = self.paste_item_data(selected_items[0], item_data)
            pasted_items.append(new_item)  # Keep track of pasted items

        # Debugging: Print what is being added to the undo stack
        print(f"Adding to undo stack: type='paste', items={pasted_items}, parent={selected_items[0]}")


        # Record the paste operation in the undo stack
        self.app.undo_stack.append({
            'type': 'paste',
            'items': pasted_items,
            'parent': selected_items[0]
        })

        self.app.copied_items = []  # Clear copied items after pasting
        self.app.tree.item(selected_items[0], open=True)
