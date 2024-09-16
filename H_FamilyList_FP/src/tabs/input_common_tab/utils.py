import tkinter as tk
from tkinter import ttk


def create_defaultTreeview(frame):
    # Define the columns for the Treeview
    columns = ("Name", "Age", "City")

    # Create the Treeview with columns
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Define the column headings
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("City", text="City")

    # Define the column properties (width, alignment)
    tree.column("Name", width=150, anchor="center")
    tree.column("Age", width=100, anchor="center")
    tree.column("City", width=150, anchor="center")

    # Insert some sample data into the tree
    tree.insert("", "end", values=("Alice", 25, "New York"))
    tree.insert("", "end", values=("Bob", 30, "Los Angeles"))
    tree.insert("", "end", values=("Charlie", 35, "Chicago"))

    # Add a scrollbar (optional)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(yscrollcommand=scrollbar.set)

    # Pack the Treeview into the window
    tree.pack(fill=tk.BOTH, expand=True)

    return tree
