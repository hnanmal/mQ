import tkinter as tk
from tkinter import ttk
import time


def load_data():
    for i in range(1, 101):  # Simulate loading with 100 items
        time.sleep(0.05)  # Simulate a time-consuming task
        tree.insert("", "end", values=(f"Item {i}", f"Value {i}"))
        progress_var.set(i)
        root.update_idletasks()  # Update UI

    progress_bar.pack_forget()  # Remove progress bar after loading is complete


root = tk.Tk()
root.title("Treeview Loading Animation Example")

# Create Treeview
tree = ttk.Treeview(root, columns=("Column 1", "Column 2"), show="headings")
tree.heading("Column 1", text="Column 1")
tree.heading("Column 2", text="Column 2")
tree.pack(pady=10)

# Progress bar to indicate loading
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=200, variable=progress_var, maximum=100
)
progress_bar.pack(pady=10)

# Load button
load_button = ttk.Button(root, text="Load Data", command=load_data)
load_button.pack(pady=10)

root.mainloop()
