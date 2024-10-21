# src/models/tree_model.py

import json
import os
from tkinter import filedialog
from src.controllers.logic import initialize_app
from src.controllers.tree_controller import extract_treeview_data
from src.views.treeview_utils import populate_treeview
from src.views.logging_utils import setup_logging_frame


def load_json_data(file_path):
    """Load JSON data from a file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print("JSON data loaded successfully.")
            return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def save_json_data(file_path, data):
    """Save data to a JSON file with UTF-8 encoding."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print("Tree view data saved successfully.")
    except Exception as e:
        print(f"Error saving JSON: {e}")


def save_treeview(state, tree):
    """Save the current state of the tree view to a JSON file."""
    save_path = filedialog.asksaveasfilename(
        defaultextension=".json", filetypes=[("JSON files", "*.json")]
    )
    state.stdType_info = tree
    if save_path:
        tree_data = extract_treeview_data(tree)
        save_json_data(save_path, tree_data)


def load_treeview(state, tree):
    """Load a new JSON file and populate the tree view."""
    load_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if load_path:
        new_data = load_json_data(load_path)
        if new_data:
            state.stdType_info = tree
            populate_treeview(tree, new_data)

    logging_text_widget = setup_logging_frame(state.root)
    initialize_app(logging_text_widget)
