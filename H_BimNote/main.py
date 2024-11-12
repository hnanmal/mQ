import tkinter as tk
from tkinter import ttk

from src.core.file_utils import load_from_json
from src.views.upper_tab import (
    create_project_apply_tab,
    create_project_standard_tab,
    create_team_standard_tab,
)
from src.views.app_ui_setup import initialize_app


def main():
    root = tk.Tk()
    notebook, state = initialize_app(root)

    # Create parent tabs within the notebook
    create_team_standard_tab(state, notebook)
    create_project_standard_tab(notebook)
    create_project_apply_tab(notebook)

    ## 팀스탠다드 자동 임포트
    load_from_json(state, "resource/PlantArch_BIM Standard.bnote")

    root.mainloop()


if __name__ == "__main__":
    main()
