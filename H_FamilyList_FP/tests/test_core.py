import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# Function to update labels in all tabs
def update_file_path_label(state, labels):
    for label in labels:
        label.config(text=f"Loaded File: {state['file_path']}")


# Function to handle file loading and state update
def load_file(state, labels):
    file_path = filedialog.askopenfilename()
    if file_path:
        state["file_path"] = file_path  # Store the file path in the state
        update_file_path_label(state, labels)  # Update the labels in all tabs


# Create the main window
root = tk.Tk()
notebook = ttk.Notebook(root)

# Shared state dictionary
state = {"file_path": "No file loaded"}

# Tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
label_tab1 = ttk.Label(tab1, text=f"Loaded File: {state['file_path']}")
label_tab1.pack(pady=10)

# Tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")
label_tab2 = ttk.Label(tab2, text=f"Loaded File: {state['file_path']}")
label_tab2.pack(pady=10)

# Tab 3 - File loading button
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Load File")
load_button = ttk.Button(
    tab3, text="Load File", command=lambda: load_file(state, [label_tab1, label_tab2])
)
load_button.pack(pady=10)

# Pack the notebook
notebook.pack(expand=True, fill="both")

root.mainloop()
