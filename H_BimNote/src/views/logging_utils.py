import tkinter as tk
from tkinter import ttk
import sys


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
    # log_text = tk.Text(logging_frame, height=8, wrap="word", state="normal")
    log_text = tk.Text(logging_frame, height=6, wrap="word", state="normal")
    log_text.pack(fill=tk.BOTH, expand=True)

    # Redirect print statements to the logging area
    redirect = RedirectText(log_text)
    sys.stdout = redirect
    sys.stderr = redirect

    return redirect  # Return the RedirectText instance
