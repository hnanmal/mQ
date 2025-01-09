import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.controllers.tree_data_navigator import TreeDataManager_treeview
from src.core.fp_utils import *
from src.views.widget.widget import StateObserver
from src.views.widget.multiline_input import MultiLineInputFrame


class ModelType_entry:
    def __init__(self, state, parent, relate_widget):
        self.state = state
        self.data_kind = "project-buildinglist"
        self.treeDataManager = TreeDataManager_treeview(state, self)
        self.relate_widget = relate_widget
        self.selected_item_relate_widget = relate_widget.selected_item
        # self.state_observer = StateObserver(state, lambda e: self.update(e))

        self.frame = ttk.Frame(parent)
        self.frame.pack(padx=10, side="left", anchor="nw")

        label_frame = ttk.Frame(self.frame)
        label_frame.pack(anchor="nw")

        widget_frame = ttk.Frame(self.frame)
        widget_frame.pack(anchor="nw")

        self.create_assign_label(label_frame)
        self.create_assign_treeview(widget_frame)

    def create_assign_label(self, frame):
        label_static = ttk.Label(frame, text="Assigned for :")
        label_static.config(font=("Arial", 12, "normal"))
        label_static.pack(padx=2, side="left", anchor="w")

        label_dynamic = ttk.Label(frame, textvariable=self.selected_item_relate_widget)
        label_dynamic.config(font=("Arial", 12, "normal"), foreground="blue")
        label_dynamic.pack(padx=2, side="left", anchor="w")

    def create_assign_treeview(self, frame):  ## 트리뷰로 할까 tksheet로 할까?
        self.rvtType_entry = MultiLineInputFrame(
            frame,
            label_text="Enter Revit Type",
        )
        self.rvtType_entry.text_widget.config(height=5)  # Change to 15 rows
        self.rvtType_entry.pack(fill="x", expand=True, padx=10, pady=10)
