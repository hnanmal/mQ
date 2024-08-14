import tkinter as tk
from tkinter import ttk


class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Binding Example")

        # Create a Notebook widget as the central widget
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Create a frame for a tab
        self.tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_frame, text="Tab 1")

        # Create the Treeview in a nested frame structure
        inner_frame = ttk.Frame(self.tab_frame)
        inner_frame.pack(fill="both", expand=True, padx=10, pady=10)

        inner_inner_frame = ttk.Frame(inner_frame)
        inner_inner_frame.pack(fill="both", expand=True)

        final_inner_frame = ttk.Frame(inner_inner_frame)
        final_inner_frame.pack(fill="both", expand=True)

        self.treeview = ttk.Treeview(final_inner_frame)
        self.treeview.pack(fill="both", expand=True)

        # Create a button that you want to trigger
        self.button = ttk.Button(
            self.tab_frame, text="Perform Action", command=self.perform_action
        )
        self.button.pack(pady=10)

        # Bind Ctrl+Space to check focus and trigger the button if the treeview has focus
        self.root.bind_all("<Control-space>", self.check_focus_and_trigger_button)

    def check_focus_and_trigger_button(self, event):
        focused_widget = self.root.focus_get()
        print("Focused widget:", focused_widget)

        # Check if the focused widget is the treeview
        if focused_widget == self.treeview:
            print("Treeview is focused; triggering button action.")
            self.button.invoke()  # Trigger the button's action

    def perform_action(self):
        print("Button action triggered!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()
