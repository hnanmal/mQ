import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("ttk Button Color Example")

# Create a style object
style = ttk.Style()

# Configure the style for TButton (ttk.Button)
style.configure("TButton", background="lightblue", foreground="black")

# Create a themed button using the custom style
button = ttk.Button(root, text="Click Me", style="TButton")
button.pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()
