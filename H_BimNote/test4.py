import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.geometry("600x400")

# Create a figure and plot
fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4], [10, 20, 25, 30])

# Embed the figure in Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

root.mainloop()
