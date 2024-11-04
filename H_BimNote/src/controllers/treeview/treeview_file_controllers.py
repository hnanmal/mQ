from tkinter import filedialog

from src.controllers.treeview.treeview_controllers import populate_treeview
from src.controllers.app_setup import initialize_app
from src.core.file_utils import load_json_data, save_json_data
from src.core.treeview_core import extract_treeview_data
from src.views.logging_utils import setup_logging_frame


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
