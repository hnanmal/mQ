import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# from ttkthemes import ThemedTk

from src.controllers.db_update_manager import DBUpdateManager
from src.core.file_utils import load_from_json
from src.views.upper_tab import (
    create_project_apply_tab,
    create_project_standard_tab,
    create_team_standard_tab,
)
from src.views.app_ui_setup import initialize_app


def main():
    # root = tk.Tk()
    root = ttk.Window(themename="journal")
    # root = ThemedTk(theme="ubuntu")
    # root = ThemedTk(theme="breeze")
    notebook, state = initialize_app(root)

    # state.db_manager = DBUpdateManager(state)
    # state.log_widget.write("!!!")
    # Create parent tabs within the notebook
    create_team_standard_tab(state, notebook)
    create_project_standard_tab(notebook)
    create_project_apply_tab(notebook)

    ## 팀스탠다드 자동 임포트
    load_from_json(state, "resource/PlantArch_BIM Standard.bnote")
    # load_from_excel(state, "resource/WorkMaster_DB.xlsx")

    ## 어플리케이션 시작시 메시지
    state.log_widget.write("어서오세요!\n")

    root.mainloop()


if __name__ == "__main__":
    main()
