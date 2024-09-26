# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import json


# def load_json_data(file_path):
#     """
#     Load data from the specified JSON file.
#     """
#     try:
#         with open(file_path, "r") as file:
#             data = json.load(file)
#         return data
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to load JSON data: {e}")
#         return {}


# def update_combobox_data(combobox, data):
#     """
#     Update the combobox values based on the data loaded from the JSON file.
#     """
#     items = data.get("items", [])

#     # Update the combobox values
#     combobox["values"] = items

#     # Set the default value to the first item if available
#     if items:
#         combobox.set(items[0])
#     else:
#         combobox.set("")  # Clear the combobox if no items are available


# def on_load_button_click():
#     """
#     Handle the load button click event.
#     """
#     # Open a file dialog to select the JSON file
#     file_path = filedialog.askopenfilename(
#         title="Open JSON File", filetypes=[("JSON Files", "*.json")]
#     )
#     if file_path:
#         # Load the JSON data and update the combobox
#         json_data = load_json_data(file_path)
#         update_combobox_data(combobox, json_data)


# # Initialize the main window
# root = tk.Tk()
# root.title("Combobox with Dynamic JSON Data")

# # Create a Combobox
# combobox = ttk.Combobox(root)
# combobox.pack(pady=10)

# # Create a button to load the JSON data
# load_button = ttk.Button(root, text="Load JSON Data", command=on_load_button_click)
# load_button.pack(pady=10)

# # Run the main loop
# root.mainloop()
