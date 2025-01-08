import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def select_tab(notebook, parent_index, subtab_index=None):
    """Select a parent tab and optionally a subtab."""
    # Disable event handlers if any
    notebook.unbind("<<NotebookTabChanged>>")

    notebook.select(parent_index)  # Select the parent tab
    if subtab_index is not None:  # If a subtab is specified
        parent_tab = notebook.nametowidget(
            notebook.tabs()[parent_index]
        )  # Get the parent tab widget
        sub_notebook = parent_tab.children.get(
            "sub_notebook"
        )  # Find the sub-notebook inside the parent tab
        if sub_notebook:
            sub_notebook.select(subtab_index)  # Select the subtab


# Composition for State Management
class StateObserver:
    def __init__(self, state, updateFunc):
        self.state = state
        self.state.observer_manager.add_observer(lambda e: updateFunc(e))


class WidgetSwitcher:
    def __init__(
        self, parent_frame, widgets, default_selection=None, default_width=300
    ):
        """
        Initialize the WidgetSwitcher.

        :param parent_frame: The parent frame where the widgets and combo box are placed.
        :param widgets: A dictionary of widget names and corresponding widgets to be switched.
        :param default_selection: The widget to display initially. Defaults to the first widget if not provided.
        """
        self.parent_frame = parent_frame
        self.widgets = (
            widgets  # A dictionary of widget names and corresponding widget objects
        )
        self.default_width = default_width

        # Create combo box for widget selection
        self.combo_box = ttk.Combobox(
            self.parent_frame, values=list(self.widgets.keys())
        )
        self.combo_box.pack(pady=10)

        # Set default selection
        if default_selection:
            self.combo_box.set(default_selection)
        else:
            # Default to the first widget in the list if none is specified
            default_widget = list(self.widgets.keys())[0]
            self.combo_box.set(default_widget)

        # Hide all widgets initially
        for widget in self.widgets.values():
            widget.pack_forget()

        # Show the default widget
        self.show_widget(self.combo_box.get())

        # Bind the combo box to the switching method
        self.combo_box.bind("<<ComboboxSelected>>", self.on_combo_box_selected)

    def show_widget(self, widget_name):
        """Show the selected widget and hide the others."""
        # Hide all widgets
        for widget in self.widgets.values():
            widget.pack_forget()

        # Show the selected widget
        selected_widget = self.widgets.get(widget_name)
        if selected_widget:
            selected_widget.pack(fill=tk.BOTH, expand=True)
            selected_widget.config(width=self.default_width)

    def on_combo_box_selected(self, event):
        """Handle the combo box selection change event."""
        selected_widget_name = self.combo_box.get()
        self.show_widget(selected_widget_name)


import tkinter as tk
from tkinter import ttk


class TabNavigationButton(tk.Frame):
    def __init__(
        self, parent, notebook, tab_index, button_text="Go to Tab", *args, **kwargs
    ):
        """
        A widget that allows navigation to a specific tab in a Tkinter notebook.

        :param parent: Parent Tkinter widget
        :param notebook: The ttk.Notebook instance to navigate
        :param tab_index: The index of the tab to navigate to
        :param button_text: The text displayed on the navigation button
        """
        super().__init__(parent, *args, **kwargs)

        self.notebook = notebook
        self.tab_index = tab_index

        # Create the navigation button
        self.button = ttk.Button(
            self,
            text=button_text,
            command=self.go_to_tab,
            # bootstyle=SUCCESS,
        )
        self.button.pack(fill="both", padx=5, pady=5)
        self.pack()

    def go_to_tab(self):
        """
        Navigate to the specified tab in the notebook.
        """
        try:
            self.notebook.select(self.tab_index)
        except tk.TclError:
            print(f"Error: Tab index {self.tab_index} is out of range.")
