import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Resizable Frames Example")

# Create a PanedWindow (horizontal orientation)
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Create three frames
frame1 = tk.Frame(paned_window, bg="lightblue", width=200, height=400)
frame2 = tk.Frame(paned_window, bg="lightgreen", width=200, height=400)
frame3 = tk.Frame(paned_window, bg="lightcoral", width=200, height=400)

# Add the frames to the PanedWindow
paned_window.add(frame1)
paned_window.add(frame2)
paned_window.add(frame3)

# Start the Tkinter event loop
root.mainloop()
