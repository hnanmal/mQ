import tkinter as tk
from ttkbootstrap import ttk, Window
from ttkbootstrap.constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


class DashboardWidget(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.init_ui()

    def init_ui(self):
        # Top Frame for Dashboard Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="Dashboard", font=("Arial", 24, "bold")).pack()

        # Main Content Frame
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True)

        # Left Panel: Stats
        stats_frame = ttk.Frame(content_frame)
        stats_frame.pack(side=LEFT, fill="y", padx=10, pady=10)

        ttk.Label(stats_frame, text="Key Metrics", font=("Arial", 18)).pack(
            anchor="w", pady=10
        )
        self.add_stat(stats_frame, "Total Users", "1,245")
        self.add_stat(stats_frame, "Active Sessions", "322")
        self.add_stat(stats_frame, "Revenue", "$10,542")

        # Right Panel: Graph
        graph_frame = ttk.Frame(content_frame)
        graph_frame.pack(side=LEFT, fill="both", expand=True, padx=10, pady=10)

        self.add_chart(graph_frame)

    def add_stat(self, parent, label, value):
        """Add a stat to the stats panel."""
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        ttk.Label(frame, text=label, font=("Arial", 12)).pack(side=LEFT)
        ttk.Label(frame, text=value, font=("Arial", 14, "bold"), bootstyle=INFO).pack(
            side=RIGHT
        )

    def add_chart(self, parent):
        """Add a chart to the graph panel."""
        # Sample data
        x = ["Jan", "Feb", "Mar", "Apr", "May"]
        y = [10, 20, 15, 25, 30]

        # Create a Matplotlib Figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y, marker="o")
        ax.set_title("Monthly Growth")
        ax.set_ylabel("Value")
        ax.set_xlabel("Month")

        # Embed the Matplotlib figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# Example Usage
if __name__ == "__main__":
    app = Window(themename="journal")
    app.title("Dashboard Example")
    app.geometry("800x600")

    dashboard = DashboardWidget(app)
    dashboard.pack(fill="both", expand=True)

    app.mainloop()
