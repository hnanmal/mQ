import tkinter as tk
from tkinter import ttk


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
