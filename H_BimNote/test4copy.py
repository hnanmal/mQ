import tkinter as tk
from tkinter import ttk
import time  # Simulate loading delay


def create_tabs():
    """Create tabs and update progress during initialization."""
    total_tabs = 5  # Total number of tabs
    for i in range(total_tabs):
        # Simulate some loading time for each tab
        time.sleep(0.5)

        # Create a new tab
        frame = tk.Frame(notebook)
        tk.Label(frame, text=f"Content of Tab {i + 1}").pack(pady=50)
        notebook.add(frame, text=f"Tab {i + 1}")

        # Update progress
        progress_value.set(
            (i + 1) / total_tabs * 100
        )  # Update progress as a percentage
        root.update_idletasks()  # Refresh the UI


# Main application window
root = tk.Tk()
root.title("Progress During Tab Creation")
root.geometry("400x300")

# Progress bar value tracker
progress_value = tk.DoubleVar()
progress_value.set(0)  # Initialize progress to 0%

# Progress bar
progress_bar = ttk.Progressbar(
    root, orient="horizontal", mode="determinate", maximum=100, variable=progress_value
)
progress_bar.pack(pady=20, fill="x", padx=20)

# Notebook (Tab container)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create tabs with progress tracking
create_tabs()

# Run the application
root.mainloop()
