# import tkinter as tk
# from tkinter import ttk


# class TreeviewWithTooltip(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Treeview with Tooltip Example")

#         # Create a Treeview widget
#         self.treeview = ttk.Treeview(self, columns=("Name", "Age"), show="headings")
#         self.treeview.heading("Name", text="Name")
#         self.treeview.heading("Age", text="Age")

#         # Insert some sample data
#         self.treeview.insert("", "end", iid="item1", values=("Alice", 30))
#         self.treeview.insert("", "end", iid="item2", values=("Bob", 25))
#         self.treeview.insert("", "end", iid="item3", values=("Charlie", 35))

#         self.treeview.pack(fill=tk.BOTH, expand=True)

#         # Dictionary to store comments/memos for each item
#         self.memos = {
#             "item1": "This is a memo for Alice.",
#             "item2": "Bob's memo goes here.",
#             "item3": "Charlie's memo is here.",
#         }

#         # Create a tooltip label (initially hidden)
#         self.tooltip = tk.Label(
#             self, bg="yellow", text="", wraplength=200, relief="solid", borderwidth=1
#         )
#         self.tooltip.place_forget()

#         # Bind motion event to the Treeview
#         self.treeview.bind("<Motion>", self.show_tooltip)

#         # Bind mouse leave event to hide the tooltip
#         self.treeview.bind("<Leave>", self.hide_tooltip)

#     def show_tooltip(self, event):
#         """Show tooltip when hovering over an item."""
#         # Identify the row (item) under the mouse pointer
#         item_id = self.treeview.identify_row(event.y)

#         # If the mouse is over an item, show the tooltip with the corresponding memo
#         if item_id and item_id in self.memos:
#             memo = self.memos[item_id]
#             self.tooltip.config(text=memo)
#             # Show the tooltip near the mouse pointer
#             self.tooltip.place(
#                 x=event.x_root - self.winfo_rootx() + 20,
#                 y=event.y_root - self.winfo_rooty() + 20,
#             )
#         else:
#             # Hide the tooltip if not hovering over an item with a memo
#             self.tooltip.place_forget()

#     def hide_tooltip(self, event):
#         """Hide the tooltip when the mouse leaves the Treeview."""
#         self.tooltip.place_forget()


# # Run the app
# app = TreeviewWithTooltip()
# app.geometry("400x300")
# app.mainloop()
