# Version: 1.0.0

from tkinter import Menu, messagebox


class ContextMenuManager:
    def __init__(self, app):
        self.app = app

    def show_context_menu(self, event):
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
        context_menu.post(event.x_root, event.y_root)

    def on_button_click(self, message):
        messagebox.showinfo("Button Clicked", message)
