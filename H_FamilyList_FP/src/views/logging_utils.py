# src/views/logging_utils.py

import tkinter as tk
from tkinter import ttk
import sys

from src.utils.tree_utils import calculate_level


class RedirectText:
    def __init__(self, text_widget):
        self.output = text_widget
        self.original_stdout = sys.stdout  # Save the original stdout

    def write(self, string):
        self.output.delete(1.0, tk.END)  # Clear existing content
        self.output.insert(tk.END, string)
        self.output.see(tk.END)  # Auto-scroll to the end
        self.original_stdout.write(string)  # Also write to the original stdout

    def flush(self):
        pass  # Needed for compatibility with some output methods


def setup_logging_frame(root):
    """Set up the logging frame at the bottom of the main window."""
    # Create a frame for logging at the bottom of the window
    logging_frame = ttk.Frame(root)
    logging_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

    # Create a Text widget for logging output
    log_text = tk.Text(logging_frame, height=8, wrap="word", state="normal")
    log_text.pack(fill=tk.BOTH, expand=True)

    # Redirect print statements to the logging area
    redirect = RedirectText(log_text)
    sys.stdout = redirect
    sys.stderr = redirect

    return redirect  # Return the RedirectText instance


def log_event_selection(tree, item, logging_widget):
    """Log the details of a tree item to the logging area."""
    item_text = tree.item(item, "text")
    item_values = tree.item(item, "values")

    # Retrieve the tags associated with the item
    item_tags = tree.item(item, "tags")

    # Prepare the log message
    log_message = f"Selected Item:\nNumber: {item_text}\n"

    if item_tags:
        log_message += f"Tags: {', '.join(item_tags)}\n"

    if item_values:
        log_message += f"Name: {item_values[0]}\nDescription: {item_values[1]}\n"

    # Write the log message to the logging widget
    logging_widget.write(log_message)


def log_event_add(tree, item, logging_widget):
    """Log the details of a tree item to the logging area."""
    item_text = tree.item(item, "text")
    item_values = tree.item(item, "values")

    # Retrieve the tags associated with the item
    item_tags = tree.item(item, "tags")

    # Prepare the log message
    log_message = f"Added Item:\nNumber: {item_text}\n"

    if item_tags:
        log_message += f"Tags: {', '.join(item_tags)}\n"

    if item_values:
        log_message += f"Name: {item_values[0]}\nDescription: {item_values[1]}\n"

    # Write the log message to the logging widget
    logging_widget.write(log_message)


# def log_event_remove(tree, item, logging_widget):
#     """Log the details of a tree item to the logging area."""
#     item_text = tree.item(item, "text")
#     item_values = tree.item(item, "values")

#     # Retrieve the tags associated with the item
#     item_tags = tree.item(item, "tags")

#     # Prepare the log message
#     log_message = f"Removed Item:\nNumber: {item_text}\n"

#     if item_tags:
#         log_message += f"Tags: {', '.join(item_tags)}\n"

#     if item_values:
#         log_message += f"Name: {item_values[0]}\nDescription: {item_values[1]}\n"

#     # Write the log message to the logging widget
#     logging_widget.write(log_message)


def log_event_remove(tree, item, logging_widget):
    """Log the details of a tree item to the logging area."""
    for item_id in item:  # Handle all items if multiple
        item_text = tree.item(item_id, "text")
        item_values = tree.item(item_id, "values")
        item_tags = tree.item(item_id, "tags")

        # Prepare the log message
        log_message = f"Removed Item:\nNumber: {item_text}\n"
        if item_tags:
            log_message += f"Tags: {', '.join(item_tags)}\n"
        if item_values:
            log_message += f"Name: {item_values[0]}\nDescription: {item_values[1]}\n"

        # Write the log message to both the terminal and the logging widget
        logging_widget.write(log_message)
