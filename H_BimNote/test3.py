# import tkinter as tk
# from tkinter import ttk


# class WidgetSwitcher:
#     def __init__(self, parent_frame, widgets, combo_box):
#         """
#         Initialize the WidgetSwitcher.

#         :param parent_frame: The parent frame where the widgets are placed.
#         :param widgets: A dictionary of widget names and corresponding widgets to be switched.
#         :param combo_box: The combo box for selecting which widget to display.
#         """
#         self.parent_frame = parent_frame
#         self.widgets = (
#             widgets  # A dictionary of widget names and corresponding widget objects
#         )
#         self.combo_box = combo_box

#         # Hide all widgets initially
#         for widget in self.widgets.values():
#             widget.pack_forget()

#         # Set default widget (if any) based on combo box selection
#         if widgets:
#             default_selection = self.combo_box.get()
#             self.show_widget(default_selection)

#         # Bind the combo box to the switching method
#         self.combo_box.bind("<<ComboboxSelected>>", self.on_combo_box_selected)

#     def show_widget(self, widget_name):
#         """Show the selected widget and hide the others."""
#         # Hide all widgets
#         for widget in self.widgets.values():
#             widget.pack_forget()

#         # Show the selected widget
#         selected_widget = self.widgets.get(widget_name)
#         if selected_widget:
#             selected_widget.pack(fill=tk.BOTH, expand=True)

#     def on_combo_box_selected(self, event):
#         """Handle the combo box selection change event."""
#         selected_widget_name = self.combo_box.get()
#         self.show_widget(selected_widget_name)


# # Example usage with two pre-created Treeview widgets
# class MainApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Widget Switcher Example")

#         # Create combo box to choose between Treeview One and Treeview Two
#         self.combobox = ttk.Combobox(self.root, values=["Treeview One", "Treeview Two"])
#         self.combobox.set("Treeview One")  # Set the default selection
#         self.combobox.pack(pady=10)

#         # Create two tree views to switch between
#         self.treeview_one = ttk.Treeview(
#             self.root, columns=("Col1", "Col2"), show="headings"
#         )
#         self.treeview_one.heading("Col1", text="Column 1")
#         self.treeview_one.heading("Col2", text="Column 2")
#         self.treeview_one.insert("", "end", values=("Item 1A", "Item 1B"))
#         self.treeview_one.insert("", "end", values=("Item 2A", "Item 2B"))

#         self.treeview_two = ttk.Treeview(
#             self.root, columns=("ColA", "ColB", "ColC"), show="headings"
#         )
#         self.treeview_two.heading("ColA", text="Column A")
#         self.treeview_two.heading("ColB", text="Column B")
#         self.treeview_two.heading("ColC", text="Column C")
#         self.treeview_two.insert("", "end", values=("Item A1", "Item B1", "Item C1"))
#         self.treeview_two.insert("", "end", values=("Item A2", "Item B2", "Item C2"))

#         # Register the widgets to switch between
#         self.widgets = {
#             "Treeview One": self.treeview_one,
#             "Treeview Two": self.treeview_two,
#         }

#         # Initialize WidgetSwitcher with the parent frame, widgets, and combo box
#         self.widget_switcher = WidgetSwitcher(self.root, self.widgets, self.combobox)


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry("600x400")
#     app = MainApp(root)
#     root.mainloop()
