import tkinter as tk


def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


root = tk.Tk()
root.geometry("300x300")

# Create a canvas and attach a scrollbar to it
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Create a frame to hold the widgets inside the canvas
scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Add the frame to the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Bind mouse wheel to scroll
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Add many widgets to the scrollable frame
for i in range(50):
    tk.Label(scrollable_frame, text=f"Label {i}").pack()

root.mainloop()
