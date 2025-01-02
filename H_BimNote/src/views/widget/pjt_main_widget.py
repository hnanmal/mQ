import tkinter as tk
from ttkbootstrap import ttk
from tksheet import Sheet

from src.views.widget.widget import StateObserver


class ProjectStdDashboard:
    def __init__(self, state, parent, *args, **kwargs):
        self.state = state  # Reference to the application state
        self.frame = ttk.Frame(parent)
        # self.data_kind = "project-stdDash"
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface for project std dashboard."""
        self.frame.config(width=600)
        self.frame.pack(side=tk.TOP, anchor="nw")

        ttk.Label(
            self.frame,
            text="Project GWM status:",
            font=("Arial", 16),
        ).pack(pady=10)

        gwm_stat = Sheet(
            self.frame,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            # headers=True,
        )
        gwm_stat.set_sheet_data(
            [
                ["지정완료 항목", 1],
                ["지정미완료 항목", 16],
                ["미사용 항목", 5],
            ]
        )
        gwm_stat.pack()

        ttk.Label(
            self.frame,
            text="Project SWM status:",
            font=("Arial", 16),
        ).pack(pady=10)

        swm_stat = Sheet(
            self.frame,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            # headers=True,
        )
        swm_stat.set_sheet_data(
            [
                ["지정완료 항목", 4],
                ["지정미완료 항목", 16],
                ["미사용 항목", 7],
            ]
        )
        swm_stat.pack()


class ProjectInfoWidget:
    # class ProjectInfoWidget(ttk.Frame):
    def __init__(self, state, parent, *args, **kwargs):
        # super().__init__(parent, *args, **kwargs)

        self.state = state  # Reference to the application state
        self.frame = ttk.Frame(parent)
        self.data_kind = "project-info"
        self.init_ui()
        self.state_observer = StateObserver(state, lambda e: self.update(e))
        self.update()  # Load data from state during initialization

    def init_ui(self):
        """Initialize the user interface for project info input."""
        self.frame.config(width=600)
        self.frame.pack(side=tk.TOP, anchor="nw")

        # Project Name
        ttk.Label(self.frame, text="Project Name:", font=("Arial", 16)).pack(pady=10)
        self.pjtName_entry = ttk.Entry(self.frame, font=("Arial", 16), bootstyle="info")
        self.pjtName_entry.pack(pady=10, padx=20, fill=tk.X)

        # Project Abbreviation
        ttk.Label(self.frame, text="Project Abbreviation:", font=("Arial", 16)).pack(
            pady=10
        )
        self.pjtAbrbr_entry = ttk.Entry(
            self.frame, font=("Arial", 16), bootstyle="info"
        )
        self.pjtAbrbr_entry.pack(pady=10, padx=20, fill=tk.X)

        # Project Type
        ttk.Label(self.frame, text="Project Type:", font=("Arial", 16)).pack(pady=10)
        self.pjtType_combobox = ttk.Combobox(
            self.frame,
            bootstyle="info",
            values=["입찰", "실행"],
            font=("Arial", 16),
        )
        self.pjtType_combobox.pack(pady=10, padx=20, fill=tk.X)

        # Update button to store changes in state
        self.update_button = ttk.Button(
            self.frame,
            text="Regiter to BNOTE",
            bootstyle="success",
            command=self.modify_state,
        )
        self.update_button.pack(pady=20)

    def modify_state(self):
        """Update state with the current input values."""
        self.state.team_std_info[self.data_kind] = {
            "name": self.pjtName_entry.get(),
            "abbr": self.pjtAbrbr_entry.get(),
            "type": self.pjtType_combobox.get(),
        }

        self.state.log_widget.write(str(self.state.team_std_info[self.data_kind]))

    def update(self, event=None):
        """Load data from the state into the input fields."""
        project_info = self.state.team_std_info.get(self.data_kind, {})
        self.state.log_widget.write(str(project_info))

        self.pjtName_entry.delete(0, tk.END)
        self.pjtName_entry.insert(0, project_info.get("name", ""))

        self.pjtAbrbr_entry.delete(0, tk.END)
        self.pjtAbrbr_entry.insert(0, project_info.get("abbr", ""))

        self.pjtType_combobox.set(project_info.get("type", ""))
