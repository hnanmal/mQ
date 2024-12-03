import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Database Setup
def initialize_db():
    conn = sqlite3.connect("treeview_items.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER,
            name TEXT NOT NULL,
            node_type TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Functions to interact with the database
def insert_item(name, parent_id=None, node_type="default"):
    conn = sqlite3.connect("treeview_items.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, parent_id, node_type) VALUES (?, ?, ?)",
        (name, parent_id, node_type),
    )
    conn.commit()
    conn.close()


def update_item(item_id, name):
    conn = sqlite3.connect("treeview_items.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ? WHERE id = ?", (name, item_id))
    conn.commit()
    conn.close()


def delete_item(item_id):
    conn = sqlite3.connect("treeview_items.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    cursor.execute(
        "DELETE FROM items WHERE parent_id = ?", (item_id,)
    )  # Delete child nodes as well
    conn.commit()
    conn.close()


def fetch_items():
    conn = sqlite3.connect("treeview_items.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, parent_id, name, node_type FROM items")
    items = cursor.fetchall()
    conn.close()
    return items


def fetch_children(parent_id):
    conn = sqlite3.connect("treeview_items.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, node_type FROM items WHERE parent_id = ?", (parent_id,)
    )
    children = cursor.fetchall()
    conn.close()
    return children


def fetch_root_items():
    conn = sqlite3.connect("treeview_items.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, node_type FROM items WHERE parent_id IS NULL")
    root_items = cursor.fetchall()
    conn.close()
    return root_items


def fetch_all_descendants(parent_id):
    descendants = []
    children = fetch_children(parent_id)
    for child in children:
        descendants.append(child)
        descendants.extend(fetch_all_descendants(child[0]))
    return descendants


# GUI Application
def run_app():
    # Initialize DB
    initialize_db()

    # Main Application Window
    root = tk.Tk()
    root.title("TreeView SQLite Editor")
    root.geometry("600x400")

    # Treeview Widget
    tree = ttk.Treeview(root)
    tree.heading("#0", text="Items", anchor="w")
    tree.pack(fill=tk.BOTH, expand=True)

    # Load Items from Database
    def load_items():
        for item in tree.get_children():
            tree.delete(item)
        items = fetch_items()
        item_dict = {}
        for item in items:
            item_id, parent_id, name, node_type = item
            if parent_id is None:
                item_dict[item_id] = tree.insert(
                    "", "end", text=f"{name} ({node_type})", tags=(str(item_id),)
                )
            else:
                item_dict[item_id] = tree.insert(
                    item_dict[parent_id],
                    "end",
                    text=f"{name} ({node_type})",
                    tags=(str(item_id),),
                )

    load_items()

    # Add Item Functionality
    def add_item():
        selected_item = tree.focus()
        new_item_name = item_name_entry.get()
        node_type = node_type_entry.get()
        if not new_item_name:
            messagebox.showwarning("Input Error", "Item name cannot be empty!")
            return
        parent_id = None
        if selected_item:
            parent_id = int(tree.item(selected_item, "tags")[0])
        insert_item(new_item_name, parent_id, node_type)
        load_items()
        item_name_entry.delete(0, tk.END)
        node_type_entry.delete(0, tk.END)

    # Edit Item Functionality
    def edit_item():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No item selected!")
            return
        new_name = item_name_entry.get()
        if not new_name:
            messagebox.showwarning("Input Error", "Item name cannot be empty!")
            return
        item_id = int(tree.item(selected_item, "tags")[0])
        update_item(item_id, new_name)
        load_items()
        item_name_entry.delete(0, tk.END)

    # Delete Item Functionality
    def delete_item_action():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No item selected!")
            return
        item_id = int(tree.item(selected_item, "tags")[0])
        delete_item(item_id)
        load_items()

    # Entry for Item Name
    item_name_entry = tk.Entry(root)
    item_name_entry.pack(fill=tk.X, padx=10, pady=5)

    # Entry for Node Type
    node_type_entry = tk.Entry(root)
    node_type_entry.pack(fill=tk.X, padx=10, pady=5)
    node_type_entry.insert(0, "default")

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    add_button = tk.Button(button_frame, text="Add Item", command=add_item)
    add_button.grid(row=0, column=0, padx=5)

    edit_button = tk.Button(button_frame, text="Edit Item", command=edit_item)
    edit_button.grid(row=0, column=1, padx=5)

    delete_button = tk.Button(
        button_frame, text="Delete Item", command=delete_item_action
    )
    delete_button.grid(row=0, column=2, padx=5)

    # Run the Tkinter Main Loop
    root.mainloop()


# Entry Point
if __name__ == "__main__":
    run_app()
