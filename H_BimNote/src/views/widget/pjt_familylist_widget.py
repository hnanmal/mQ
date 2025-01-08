import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tksheet import Sheet
from tkinter import messagebox

from src.views.widget.treeview_utils import TeamStd_FamlistTreeView


class StdFamilyListWidget(tk.Frame):
    def __init__(self, state, parent, *args, **kwargs):
        self.state = state
        # self.init_ui()
        frame = ttk.Frame(parent)
        frame.pack()

        self.set_familylist(frame)

    def set_familylist(self, parent):
        teamStd_FamlistTreeView = TeamStd_FamlistTreeView(
            self.state,
            parent,
            title="Family List: 레빗타입을 할당할 대상을 선택해주세요",
            showmode="project_assign",
        )

        teamStd_FamlistTreeView.treeview.tree.column(
            0, width=0, minwidth=0, stretch=False
        )
        # teamStd_FamlistTreeView.treeview.tree.column(
        #     "GWM/SWM", width=0, minwidth=0, stretch=False
        # )
        teamStd_FamlistTreeView.treeview.tree.column(
            "Item", width=0, minwidth=0, stretch=False
        )
        teamStd_FamlistTreeView.treeview.tree.column(
            "표준산출 수식", width=0, minwidth=0, stretch=False
        )
        teamStd_FamlistTreeView.treeview.tree.column(
            "Description", width=0, minwidth=0, stretch=False
        )
