# src/views/treeview_handlers.py

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from src.controllers.tree_controller import on_item_select
from src.views.menu import generate_context_menu
from src.views.styles import configure_styles
from src.controllers.clipboard_management import (
    copy_to_clipboard,
    paste_from_clipboard,
    paste_external_data,
)
from src.utils.tree_utils import extract_treeview_data


def create_treeview(parent, state):
    """Create a tree view widget with a hierarchical number column and a vertical scrollbar."""

    # Function to scroll to the selected item when the spacebar is pressed
    def scroll_to_selected_item(event, tree):
        selected_item = tree.selection()
        if selected_item:
            tree.see(selected_item[0])  # Ensure the selected item is visible

    # Create a frame to hold the treeview and scrollbar
    tree_frame = ttk.Frame(parent)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create horizontal scrollbar
    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a tree view widget with a hierarchical number column.
    tree = ttk.Treeview(
        tree_frame,
        columns=("name", "description"),
        show="tree headings",
        yscrollcommand=v_scrollbar.set,
        xscrollcommand=h_scroll.set,
    )

    # Set up the columns
    tree.heading("#0", text="Number", anchor="w")
    tree.heading("name", text="Name", anchor="w")
    tree.heading("description", text="Description", anchor="w")

    # Configure the columns
    tree.column("#0", width=220, minwidth=220, stretch=False, anchor="w")
    tree.column("name", width=200, anchor="w")
    tree.column("description", width=300, anchor="w")

    tree.pack(fill=tk.BOTH, expand=True)

    # Configure the scrollbar
    v_scrollbar.config(command=tree.yview)

    # Apply the custom styles
    configure_styles(tree)

    # Bind the selection event
    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: on_item_select(event, state),
    )

    tree.bind("<space>", lambda e: scroll_to_selected_item(e, tree))

    # Bind the right-click event
    tree.bind("<Button-3>", lambda event: on_right_click(event, state, tree))

    tree.bind("<Control-c>", lambda event: handle_copy(tree, event, state))
    tree.bind("<Control-v>", lambda event: handle_paste(tree, event, state))

    tree.update_idletasks()
    return tree


def create_treeview_forPjinfo(parent, state):
    """Create a tree view widget with a hierarchical number column and a vertical scrollbar."""
    # Create a frame to hold the treeview and scrollbar
    tree_frame = ttk.Frame(parent)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create horizontal scrollbar
    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a tree view widget with a hierarchical number column.
    tree = ttk.Treeview(
        tree_frame,
        columns=("number", "name", "description"),
        show="tree headings",
        yscrollcommand=v_scrollbar.set,
        xscrollcommand=h_scroll.set,
    )

    # Set up the columns
    tree.heading("number", text="Number", anchor="w")
    tree.heading("name", text="Name", anchor="w")
    tree.heading("description", text="Description", anchor="w")

    # Configure the columns
    tree.column("number", width=220, minwidth=220, stretch=False, anchor="w")
    tree.column("name", width=200, anchor="w")
    tree.column("description", width=300, anchor="w")

    tree.pack(fill=tk.BOTH, expand=True)

    # Configure the scrollbar
    v_scrollbar.config(command=tree.yview)

    # Apply the custom styles
    configure_styles(tree)

    # Bind the selection event
    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: on_item_select(event, state),
    )

    # Bind the right-click event
    tree.bind("<Button-3>", lambda event: on_right_click(event, state, tree))

    tree.bind("<Control-c>", lambda event: handle_copy(tree, event, state))
    tree.bind("<Control-v>", lambda event: handle_paste(tree, event, state))

    tree.update_idletasks()
    return tree


def on_right_click(event, state, tree):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if item and column:
        menu = generate_context_menu(state, tree, item, column)
        menu.post(event.x_root, event.y_root)


def handle_copy(tree, event, state):
    try:
        selected_items = tree.selection()
        # 디버깅: 선택된 항목 확인
        print(f"Selected items for copy: {selected_items}")

        if selected_items:
            copy_to_clipboard(tree, selected_items, state)
            print(f"Items copied: {selected_items}")
    except Exception as e:
        print(f"Error during copy: {e}")


def handle_paste(tree, event, state):
    clipboard_data = state.get_clipboard_data()
    # 상태 객체에서 클립보드 데이터를 가져옴
    print(f"Clipboard data before paste: {clipboard_data}")

    selected_items = tree.selection()
    print(f"selected_items: {selected_items}")

    # 트리뷰 복사 및 붙여넣기 처리
    if selected_items:
        if clipboard_data:  # 클립보드에 트리뷰 데이터가 있는지 확인
            print("Pasting within TreeView")  # 디버깅 라인
            # paste_from_clipboard(tree, selected_items[0])
            for target_item in selected_items:
                paste_from_clipboard(tree, selected_items, clipboard_data)
        else:
            # 외부 소스에서 데이터 붙여넣기
            print("Pasting from external source")  # 디버깅 라인
            paste_target_items = selected_items
            paste_to = (
                ask_paste_location()
            )  # 붙여넣기 위치 선택 (Name 또는 Description)
            if paste_to:
                paste_external_data(tree, paste_target_items, paste_to)


class PasteLocationDialog(simpledialog.Dialog):
    def body(self, master):
        self.var = tk.StringVar(value="name")

        tk.Label(master, text="Where do you want to paste the text?").pack(pady=10)

        self.name_radio = tk.Radiobutton(
            master, text="Name", variable=self.var, value="name"
        )
        self.name_radio.pack(anchor="w")

        self.description_radio = tk.Radiobutton(
            master, text="Description", variable=self.var, value="description"
        )
        self.description_radio.pack(anchor="w")

        return self.name_radio  # Initial focus

    def apply(self):
        self.result = self.var.get()


def ask_paste_location():
    """Prompt user to select whether to paste into Name or Description."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    dialog = PasteLocationDialog(root, "Paste Location")
    return dialog.result
