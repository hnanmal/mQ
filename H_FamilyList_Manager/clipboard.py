# Version: 1.0.0

import pyperclip


class ClipboardManager:
    def __init__(self, app):
        self.app = app

    def copy_to_clipboard(self, event=None):
        if self.app.is_text_editing:
            return  # Skip clipboard operation if in text editing mode
        selected_items = self.app.tree.selection()
        if not selected_items:
            self.app.messagebox.showwarning(
                "No Selection", "Please select an item to copy."
            )
            return
        clipboard_data = "\n".join(
            [self.app.original_names[item] for item in selected_items]
        )
        pyperclip.copy(clipboard_data)
        self.app.messagebox.showinfo("Copy", "Selected items copied to clipboard.")

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
                        self.app.config_manager.update_displayed_name(
                            item
                        )  # Update displayed name with the new value
                    elif target_column == "Description":
                        self.app.tree.set(
                            item, "description", text
                        )  # Update the description
                return
