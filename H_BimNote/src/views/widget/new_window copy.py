import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

from src.views.lower_tabs.pjt_apply_main_tab import create_pjtApply_Main_tab
from src.views.app_ui_setup import initialize_app


# def open_tab_in_new_window(parent_notebook, tab_index):
def open_tab_in_new_window(state, _notebook, tab_funcs, event=None):
    """Open the contents of a specific tab in a new window."""
    # Create a new window
    root = state.root
    new_window = tk.Toplevel(root)
    # new_window = tk.Toplevel()
    new_window.title("Rvt Summary Window")
    new_window.geometry("1000x900")

    # Set the new window to always be on top
    new_window.attributes("-topmost", True)

    # state = initialize_app(new_window, _state=state)

    # Get the index of the clicked tab
    clicked_tab_index = _notebook.index("@%d,%d" % (event.x, event.y))
    tab_func = tab_funcs[clicked_tab_index]
    tab_func(state, new_window, exe_mode="new_window")  # .pack()

    # # Clone the tab's content into the new window
    # selected_tab = parent_notebook.nametowidget(parent_notebook.tabs()[tab_index])
    # new_content_frame = ttk.Frame(new_window)
    # new_content_frame.pack(fill=tk.BOTH, expand=True)

    # for child in selected_tab.winfo_children():
    #     child_clone = clone_widget(child, new_content_frame)
    #     child_clone.pack(fill=tk.BOTH, expand=True)


def clone_widget(widget, parent):
    """Clone a widget into a new parent."""
    # Clone a Frame (simplifies cloning for this example)
    if isinstance(widget, ttk.Frame):
        new_frame = ttk.Frame(parent)
        for child in widget.winfo_children():
            clone_widget(child, new_frame)
        return new_frame

    # Handle other widgets (e.g., Button, Label)
    widget_class = widget.winfo_class()
    if widget_class == "TButton":
        return ttk.Button(parent, text=widget["text"], command=widget["command"])
    elif widget_class == "TLabel":
        return ttk.Label(parent, text=widget["text"])
    # Extend for other widget types as needed
    return None


# Example App
def main():
    root = tk.Tk()
    root.geometry("600x400")
    style = Style("cosmo")

    # Create a Notebook with tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Tab 1
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Tab 1")
    ttk.Label(tab1, text="This is Tab 1").pack(padx=10, pady=10)

    # Tab 2
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Tab 2")
    ttk.Label(tab2, text="This is Tab 2").pack(padx=10, pady=10)

    # Add a button to open Tab 1 in a new window
    open_button = ttk.Button(
        root,
        text="Open Tab 1 in New Window",
        command=lambda: open_tab_in_new_window(notebook, 0),
    )
    open_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
