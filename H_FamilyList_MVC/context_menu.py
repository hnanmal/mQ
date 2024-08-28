# Version: 1.0.0

from tkinter import Menu, messagebox


class ContextMenuManager:
    def __init__(self, app):
        self.app = app
        self.app.tree.bind(
            "<Button-3>",
            self.show_context_menu,
        )

    def show_context_menu(self, event):
        print("Right-click detected")  # 디버그 로그
        context_menu = Menu(self.app, tearoff=0)
        context_menu.add_command(
            label="Copy", command=self.app.clipboard_manager.copy_selected_items
        )
        context_menu.add_command(
            label="Paste", command=self.app.clipboard_manager.paste_copied_items
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="상위레벨로",
            command=self.app.drag_and_drop_manager.move_items_up_one_level,
        )
        context_menu.add_command(
            label="하위레벨로",
            command=self.app.drag_and_drop_manager.move_items_down_one_level,
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="Group Under WM_group1",
            command=self.group_selected_items_under_new_parent,
        )
        context_menu.post(event.x_root, event.y_root)
        # context_menu.tk_popup(event.x_root, event.y_root)

    def group_selected_items_under_new_parent(self):
        selected_items = self.app.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select items to group.")
            return

        # Determine the common parent of the selected items
        common_parent = self.app.tree.parent(selected_items[0])
        for item in selected_items:
            if self.app.tree.parent(item) != common_parent:
                messagebox.showwarning(
                    "Invalid Selection", "Selected items must share the same parent."
                )
                return

        # Find the index of the first selected item
        first_selected_item = selected_items[0]
        first_item_index = self.app.tree.index(first_selected_item)

        # Create the WM_group1 item before the first selected item
        new_group_number = (
            self.app.tree.item(common_parent, "text") + f".{first_item_index + 1}"
        )
        new_parent = self.app.tree.insert(
            common_parent,
            first_item_index,
            text=new_group_number,
            values=("WM_group1", ""),
        )

        # Store the original name
        self.app.original_names[new_parent] = "WM_group1"

        # Move each selected item under the new parent
        for item in selected_items:
            self.app.tree.move(item, new_parent, "end")
            self.app.treeview_operations.update_displayed_name(item)

        # Ensure the new parent is visible and expanded
        self.app.tree.see(new_parent)
        self.app.tree.item(common_parent, open=True)
        self.app.tree.item(new_parent, open=True)

        # Renumber children of the common parent to reflect the new structure
        self.app.treeview_operations.renumber_children(common_parent)

        # Force a UI update to reflect changes
        self.app.update_idletasks()

        # Add this operation to the undo stack
        undo_data = {"type": "group", "new_parent": new_parent, "items": []}
        for item in selected_items:
            original_parent = self.app.tree.parent(item)
            original_index = self.app.tree.index(item)
            undo_data["items"].append(
                {
                    "item": item,
                    "original_parent": original_parent,
                    "original_index": original_index,
                }
            )
        self.app.undo_stack.append(undo_data)

        # Reselect the new parent or the grouped items
        self.app.tree.selection_set(new_parent)

    def on_button_click(self, message):
        messagebox.showinfo("Button Clicked", message)
