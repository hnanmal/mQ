# src/views/widget/sheet_utils.py
from src.controllers.tree_data_navigator import (
    TreeDataManager_treesheet,
    TreeDataManager_treeview,
)
from src.core.fp_utils import *
import tkinter as tk
from tkinter import ttk, simpledialog
from tksheet import Sheet

from src.controllers.widget.widgets import toggle_stdGWM_widget_mode
from src.views.widget.widget import StateObserver
from src.views.widget.treesheet_editor import TreesheetEditor
import uuid


class DefaultSheetViewStyleManager:
    pass


class SheetViewStateObserver:
    def __init__(self, state, treeview, updateFunc):
        self.state = state
        self.state.observer_manager.add_observer(updateFunc)


class SheetSearchManager:
    def __init__(self, sheet, state):
        self.sheet = sheet
        self.state = state
        # self.original_data = sheet.get_sheet_data(return_copy=True)

    def search_sheet_data(self, search_term):
        """Search for rows containing the search term and update the sheet."""
        search_term = search_term.lower()
        if not search_term:
            # If the search term is empty, reset to the original data
            self.reset_sheet_data()
            return

        # Get all data from the sheet and filter it
        all_data = self.state.team_std_info.get("WMs", [])
        filtered_data = [
            row
            for row in all_data
            if any(search_term in str(cell).lower() for cell in row)
        ]

        # Update the sheet with filtered data
        self.sheet.set_sheet_data(filtered_data)

    def reset_sheet_data(self):
        """Reset the sheet to its original state."""
        original_data = self.state.team_std_info.get("WMs", [])
        self.sheet.set_sheet_data(original_data)

    def reset_search(self, search_entry):
        """Clear the search entry and reset the sheet data to the original state."""
        search_entry.delete(0, tk.END)  # Clear the search entry
        self.reset_sheet_data()  # Reset the data in the sheet


class BaseSheetView:
    def __init__(self, parent, headers):
        self.sheet = Sheet(parent, headers=headers)
        self.parent = parent

        # config enable_bindings
        self.sheet.enable_bindings(
            "edit_cell",
            "delete",
            "single_select",  # Allow single cell selection
            "drag_select",
            "row_select",  # Allow row selection
            "column_select",  # Allow column selection
            "drag_select",  # Allow drag selection
            "column_width_resize",
            "row_height_resize",
            "double_click_column_resize",
            "copy",
            "paste",
            "ctrl_click_select",
            "right_click_popup_menu",
            "rc_insert_row",
            "rc_delete_row",
            "arrowkeys",
        )

    def setup_columns(self, headers, hdr_widths=None):
        pass

    def insert_data(self, data):
        pass

    def clear_sheetview():
        pass

    def get_sheet_data():
        pass


class ProjectStd_WM_Selcet_SheetView_GWM:
    def __init__(self, state, parent, relate_widget):
        self.state = state
        self.data_kind = "std-GWM"
        self.treeDataManager = TreeDataManager_treesheet(state, self)
        self.relate_widget = relate_widget
        self.selected_item_relate_widget = relate_widget.selected_item
        self.sheet = Sheet(
            parent,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            width=2000,
            height=800,
        )
        self.sheet.pack(expand=True, fill="both", padx=5, pady=5)

        # config enable_bindings
        self.sheet.enable_bindings(
            "edit_cell",
            "delete",
            "single_select",  # Allow single cell selection
            "drag_select",
            "row_select",  # Allow row selection
            "column_select",  # Allow column selection
            "drag_select",  # Allow drag selection
            "column_width_resize",
            "row_height_resize",
            "double_click_column_resize",
            "copy",
            "paste",
            "ctrl_click_select",
            "right_click_popup_menu",
            "rc_insert_row",
            "rc_delete_row",
            "arrowkeys",
        )

        # Bind checkbox clicks
        self.sheet.extra_bindings(
            [
                ("end_edit_cell", lambda e: self.on_checkbox_click(e)),
            ]
        )

        # 초기 데이터 로드 및 시트 설정
        self.setup_sheet()

        # 상태 변경 감지를 위한 옵저버 설정
        self.state_observer = StateObserver(state, lambda e: self.update(e))

    def setup_sheet(self):
        # 헤더 설정
        headers = ["Use", "Spec", "Unit", "Work Master"]
        self.sheet.headers(headers)

        # Create checkboxes in the First column
        self.sheet.checkbox("A", checked=True)

        self.setup_column_style()
        # 초기 데이터 로드
        self.update()

    def setup_column_style(self):
        # self.sheet.set_column_widths([25, 200, 25, 2000])
        self.sheet.set_column_widths([25, 200, 25, 1000])

        self.sheet["A"].align("center")
        self.sheet.set_options(header_font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(font=("Arial", 10, "normal"))

        # self.sheet.set_options(default_row_height=40)

    def on_checkbox_click(self, event):
        """Callback for checkbox clicks."""
        self.state.log_widget.write(
            f"{self.__class__.__name__} > on_checkbox_click 메소드 시작"
        )
        selected_item_str = self.selected_item_relate_widget.get()
        project_GWM = self.state.team_std_info["project-GWM"].get(selected_item_str)

        # print(self.sheet.get_data())

        row = event["row"]
        column = event["column"]
        for r in range(self.sheet.get_total_rows()):
            if r != row:
                self.sheet.set_cell_data(r, 0, False)  # Uncheck other rows

        # Ensure the clicked checkbox remains selected
        self.sheet.set_cell_data(row, 0, True)

        loc = list(event["cells"]["table"].keys())[0]
        row_check_status = event["value"]

        self.state.log_widget.write(f"위치: {loc}, 체크스테이터스 : {row_check_status}")

        wm_code = self.sheet.get_cell_data(row, 3).split(" | ")[0]

        if column == 0:
            if project_GWM:
                spec = project_GWM[-1]
                unit = project_GWM[-2]
            else:
                spec = go(
                    self.sheet.get_cell_data(row, 3),
                    lambda x: x.replace("\n", ""),
                    lambda x: x.split(" | "),
                    filter(lambda x: ("(   )" in x) or ("(   )" in x) or ("(  )" in x)),
                    lambda x: "\n".join(x),
                )
            unit = go(
                self.sheet.get_cell_data(row, 3),
                lambda x: x.replace("\n", ""),
                lambda x: x.split(" | ")[-3],
            )
        elif column == 1:
            spec = event["value"]
            unit = go(
                self.sheet.get_cell_data(row, 3),
                lambda x: x.replace("\n", ""),
                lambda x: x.split(" | ")[-3],
            )

        # if row_check_status:
        self.state.team_std_info["project-GWM"].update(
            {selected_item_str: [wm_code, unit, spec]}
        )
        self.state.log_widget.write(
            self.state.team_std_info["project-GWM"][selected_item_str]
        )
        self.highlight_checked_row()

    def highlight_checked_row(self):
        """Update row highlights based on checkbox values."""
        checked_rows = []
        for row in range(self.sheet.get_total_rows()):
            if self.sheet.get_cell_data(row, 0):  # If checkbox is checked
                checked_rows.append(row)

        # Clear existing highlights
        self.sheet.dehighlight_all()
        self.sheet.highlight_rows(
            checked_rows, highlight_index=False, bg="#D3F9D8"
        )  # Light green

    def wrap_text(self, text, width):
        """
        Wrap text to fit within a given width, handling long words properly.
        """
        if not text or not isinstance(text, str):
            return text
        max_chars_per_line = max(1, width // 7)  # Approximate character width in pixels

        words = text.split()  # Split into words
        lines = []
        current_line = ""

        for word in words:
            while len(word) > max_chars_per_line:  # Split long words into chunks
                lines.append(word[:max_chars_per_line])
                word = word[max_chars_per_line:]

            if len(current_line) + len(word) + 1 > max_chars_per_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = f"{current_line} {word}".strip()

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    def apply_wrap(self, tgt_idx, tgt_width=None):
        """
        Apply wrapping to all cells based on their column widths.
        """
        wrapped_data = []
        # for row_index, row in enumerate(self.sheet.get_sheet_data()):
        for row_index, row in enumerate(self.sheet.get_sheet_data()):
            wrapped_row = []
            for col_index, cell in enumerate(row):
                if col_index == tgt_idx:
                    if tgt_width:
                        width = tgt_width
                    else:
                        width = self.sheet.column_width(col_index)
                    wrapped_row.append(self.wrap_text(cell, width))
                else:
                    wrapped_row.append(cell)
            wrapped_data.append(wrapped_row)

        print(f"col width: {width}")
        # print(f"시트 data: {self.sheet.get_sheet_data()}")
        # print(f"시트 분할문자: {wrapped_data}")
        self.sheet.set_sheet_data(wrapped_data)

    def update(self, event=None):
        state = self.state
        """Update the TreeView whenever the state changes."""
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")
        self.state.log_widget.write(
            f"선택아이템 출력 : {self.selected_item_relate_widget.get()}"
        )
        self.setup_column_style()

        try:
            # Split the selected item path to find the grandparent, parent, and selected item names
            grand_parent_item_name, parent_item_name, selected_item_name = (
                self.selected_item_relate_widget.get().split(" | ")
            )

            # Ensure the data kind exists in the team standard information
            if self.data_kind in state.team_std_info:
                data = state.team_std_info[self.data_kind]["children"]

                # Find the grandparent node
                grand_parent_node = next(
                    (node for node in data if node["name"] == grand_parent_item_name),
                    None,
                )
                if grand_parent_node:
                    # Find the parent node
                    parent_node = next(
                        (
                            node
                            for node in grand_parent_node["children"]
                            if node["name"] == parent_item_name
                        ),
                        None,
                    )
                    if parent_node:
                        # Find the selected node
                        selected_node = next(
                            (
                                node
                                for node in parent_node["children"]
                                if node["name"] == selected_item_name
                            ),
                            None,
                        )
                        if selected_node:
                            # Clear the TreeView and insert the data for the selected node
                            self.sheet.clear()

                            # Wrap the children of the selected node for insertion
                            wrapped_data = go(
                                selected_node["children"],
                                map(
                                    lambda x: [
                                        "",
                                        go(
                                            x.split(" | "),
                                            filter(
                                                lambda x: ("(   )" in x)
                                                or ("(   )" in x)
                                                or ("(  )" in x)
                                            ),
                                            lambda x: "\n".join(x),
                                        ),
                                        x.split(" | ")[-3],
                                        x,
                                    ]
                                ),
                                list,
                            )

                            selected_item_str = self.selected_item_relate_widget.get()
                            decided_WM = state.team_std_info["project-GWM"].get(
                                selected_item_str, None
                            )

                            tgt_rowIdx = 0
                            if decided_WM:
                                for idx, row in enumerate(wrapped_data):
                                    if decided_WM[0] in row[-1]:
                                        row[0] = True
                                        row[1] = decided_WM[-1]
                                        row[2] = decided_WM[-2]
                                        tgt_rowIdx = idx

                            # self.treeview.insert_data_with_levels(wrapped_data)
                            self.sheet.set_sheet_data(wrapped_data)

                            ###########test#################
                            self.apply_wrap(tgt_idx=3, tgt_width=1000)
                            self.sheet.set_all_cell_sizes_to_text()
                            self.sheet.set_all_row_heights(
                                height=50,
                                only_set_if_too_small=True,
                            )
                            ###########test#################

                            self.sheet.see(tgt_rowIdx, 0)
                        else:
                            self.state.log_widget.write(
                                f"Selected item '{selected_item_name}' not found."
                            )
                    else:
                        self.state.log_widget.write(
                            f"Parent item '{parent_item_name}' not found."
                        )
                else:
                    self.state.log_widget.write(
                        f"Grandparent item '{grand_parent_item_name}' not found."
                    )

        except Exception as e:
            self.state.log_widget.write(
                f"{self.__class__.__name__} > update 메소드 진입 안됩니다~: {e}"
            )

        self.setup_column_style()
        self.highlight_checked_row()

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def set_edit_mode(self, mode):
        # 편집 모드 설정
        if mode == "edit":
            self.sheet.enable_bindings()
        else:
            self.sheet.disable_bindings()


class ProjectStd_WM_Selcet_SheetView_SWM:
    def __init__(self, state, parent, relate_widget):
        self.state = state
        self.data_kind = "std-SWM"
        self.treeDataManager = TreeDataManager_treesheet(state, self)
        self.relate_widget = relate_widget
        self.selected_item_relate_widget = relate_widget.selected_item
        self.sheet = Sheet(
            parent,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            width=2000,
            height=800,
        )
        self.sheet.pack(expand=True, fill="both", padx=5, pady=5)

        # config enable_bindings
        self.sheet.enable_bindings(
            "edit_cell",
            "delete",
            "single_select",  # Allow single cell selection
            "drag_select",
            "row_select",  # Allow row selection
            "column_select",  # Allow column selection
            "drag_select",  # Allow drag selection
            "column_width_resize",
            "row_height_resize",
            "double_click_column_resize",
            "copy",
            "paste",
            "ctrl_click_select",
            "right_click_popup_menu",
            "rc_insert_row",
            "rc_delete_row",
            "arrowkeys",
        )

        # Bind checkbox clicks
        self.sheet.extra_bindings(
            [
                ("end_edit_cell", lambda e: self.on_checkbox_click(e)),
            ]
        )

        # 초기 데이터 로드 및 시트 설정
        self.setup_sheet()

        # 상태 변경 감지를 위한 옵저버 설정
        self.state_observer = StateObserver(state, lambda e: self.update(e))

    def setup_sheet(self):
        # 헤더 설정
        headers = ["Use", "Spec", "Unit", "Work Master"]
        self.sheet.headers(headers)

        # Create checkboxes in the First column
        self.sheet.checkbox("A", checked=True)

        self.setup_column_style()
        # 초기 데이터 로드
        self.update()

    def setup_column_style(self):
        # self.sheet.set_column_widths([25, 200, 25, 2000])
        self.sheet.set_column_widths([25, 200, 25, 1000])

        self.sheet["A"].align("center")
        self.sheet.set_options(header_font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(font=("Arial", 10, "normal"))

        # self.sheet.set_options(default_row_height=30)

    def on_checkbox_click(self, event):
        """Callback for checkbox clicks."""
        self.state.log_widget.write(
            f"{self.__class__.__name__} > on_checkbox_click 메소드 시작"
        )
        selected_item_str = self.selected_item_relate_widget.get()
        project_SWM = self.state.team_std_info["project-SWM"].get(selected_item_str)

        # print(self.sheet.get_data())

        row = event["row"]
        column = event["column"]
        for r in range(self.sheet.get_total_rows()):
            if r != row:
                self.sheet.set_cell_data(r, 0, False)  # Uncheck other rows

        # Ensure the clicked checkbox remains selected
        self.sheet.set_cell_data(row, 0, True)

        loc = list(event["cells"]["table"].keys())[0]
        row_check_status = event["value"]

        self.state.log_widget.write(f"위치: {loc}, 체크스테이터스 : {row_check_status}")

        wm_code = self.sheet.get_cell_data(row, 3).split(" | ")[0]

        if column == 0:
            if project_SWM:
                spec = project_SWM[-1]
                unit = project_SWM[-2]
            else:
                spec = go(
                    self.sheet.get_cell_data(row, 3),
                    lambda x: x.replace("\n", ""),
                    lambda x: x.split(" | "),
                    filter(lambda x: ("(   )" in x) or ("(   )" in x) or ("(  )" in x)),
                    lambda x: "\n".join(x),
                )
                unit = go(
                    self.sheet.get_cell_data(row, 3),
                    lambda x: x.replace("\n", ""),
                    lambda x: x.split(" | ")[-3],
                )
            # unit = self.sheet.get_cell_data(row, 3).split(" | ")[-3]
        elif column == 1:
            spec = event["value"]
            unit = go(
                self.sheet.get_cell_data(row, 3),
                lambda x: x.replace("\n", ""),
                lambda x: x.split(" | ")[-3],
            )

        # if row_check_status:
        self.state.team_std_info["project-SWM"].update(
            {selected_item_str: [wm_code, unit, spec]}
        )
        self.state.log_widget.write(
            self.state.team_std_info["project-SWM"][selected_item_str]
        )
        self.highlight_checked_row()

    def highlight_checked_row(self):
        """Update row highlights based on checkbox values."""
        checked_rows = []
        for row in range(self.sheet.get_total_rows()):
            if self.sheet.get_cell_data(row, 0):  # If checkbox is checked
                checked_rows.append(row)

        # Clear existing highlights
        self.sheet.dehighlight_all()
        self.sheet.highlight_rows(
            checked_rows, highlight_index=False, bg="#D3F9D8"
        )  # Light green

    def wrap_text(self, text, width):
        """
        Wrap text to fit within a given width, handling long words properly.
        """
        if not text or not isinstance(text, str):
            return text
        max_chars_per_line = max(1, width // 7)  # Approximate character width in pixels

        words = text.split()  # Split into words
        lines = []
        current_line = ""

        for word in words:
            while len(word) > max_chars_per_line:  # Split long words into chunks
                lines.append(word[:max_chars_per_line])
                word = word[max_chars_per_line:]

            if len(current_line) + len(word) + 1 > max_chars_per_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = f"{current_line} {word}".strip()

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    def apply_wrap(self, tgt_idx, tgt_width=None):
        """
        Apply wrapping to all cells based on their column widths.
        """
        wrapped_data = []
        # for row_index, row in enumerate(self.sheet.get_sheet_data()):
        for row_index, row in enumerate(self.sheet.get_sheet_data()):
            wrapped_row = []
            for col_index, cell in enumerate(row):
                if col_index == tgt_idx:
                    if tgt_width:
                        width = tgt_width
                    else:
                        width = self.sheet.column_width(col_index)
                    wrapped_row.append(self.wrap_text(cell, width))
                else:
                    wrapped_row.append(cell)
            wrapped_data.append(wrapped_row)

        print(f"col width: {width}")
        # print(f"시트 data: {self.sheet.get_sheet_data()}")
        # print(f"시트 분할문자: {wrapped_data}")
        self.sheet.set_sheet_data(wrapped_data)

    def update(self, event=None):
        state = self.state
        """Update the TreeView whenever the state changes."""
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")
        self.state.log_widget.write(
            f"선택아이템 출력 : {self.selected_item_relate_widget.get()}"
        )

        try:
            # Split the selected item path to find the grandparent, parent, and selected item names
            grand_parent_item_name, parent_item_name, selected_item_name = (
                self.selected_item_relate_widget.get().split(" | ")
            )

            # Ensure the data kind exists in the team standard information
            if self.data_kind in state.team_std_info:
                data = state.team_std_info[self.data_kind]["children"]

                # Find the grandparent node
                grand_parent_node = next(
                    (node for node in data if node["name"] == grand_parent_item_name),
                    None,
                )
                if grand_parent_node:
                    # Find the parent node
                    parent_node = next(
                        (
                            node
                            for node in grand_parent_node["children"]
                            if node["name"] == parent_item_name
                        ),
                        None,
                    )
                    if parent_node:
                        # Find the selected node
                        selected_node = next(
                            (
                                node
                                for node in parent_node["children"]
                                if node["name"] == selected_item_name
                            ),
                            None,
                        )
                        if selected_node:
                            # Clear the TreeView and insert the data for the selected node
                            self.sheet.clear()

                            # Wrap the children of the selected node for insertion
                            wrapped_data = go(
                                selected_node["children"],
                                map(
                                    lambda x: [
                                        "",
                                        go(
                                            x.split(" | "),
                                            filter(
                                                lambda x: ("(   )" in x)
                                                or ("(   )" in x)
                                                or ("(  )" in x)
                                            ),
                                            lambda x: "\n".join(x),
                                        ),
                                        x.split(" | ")[-3],
                                        x,
                                    ]
                                ),
                                list,
                            )

                            selected_item_str = self.selected_item_relate_widget.get()
                            decided_WM = state.team_std_info["project-SWM"].get(
                                selected_item_str, None
                            )

                            tgt_rowIdx = 0
                            if decided_WM:
                                for idx, row in enumerate(wrapped_data):
                                    if decided_WM[0] in row[-1]:
                                        row[0] = True
                                        row[1] = decided_WM[-1]
                                        row[2] = decided_WM[-2]
                                        tgt_rowIdx = idx

                            # self.treeview.insert_data_with_levels(wrapped_data)
                            self.sheet.set_sheet_data(wrapped_data)

                            ###########test#################
                            self.apply_wrap(tgt_idx=3, tgt_width=1000)
                            self.sheet.set_all_cell_sizes_to_text()
                            self.sheet.set_all_row_heights(
                                height=50,
                                only_set_if_too_small=True,
                            )
                            ###########test#################

                            self.sheet.see(tgt_rowIdx, 0)
                        else:
                            self.state.log_widget.write(
                                f"Selected item '{selected_item_name}' not found."
                            )
                    else:
                        self.state.log_widget.write(
                            f"Parent item '{parent_item_name}' not found."
                        )
                else:
                    self.state.log_widget.write(
                        f"Grandparent item '{grand_parent_item_name}' not found."
                    )

        except Exception as e:
            self.state.log_widget.write(
                f"{self.__class__.__name__} > update 메소드 진입 안됩니다~: {e}"
            )

        self.setup_column_style()
        self.highlight_checked_row()

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def set_edit_mode(self, mode):
        # 편집 모드 설정
        if mode == "edit":
            self.sheet.enable_bindings()
        else:
            self.sheet.disable_bindings()


class TeamStd_WMsSheetView:
    def __init__(self, state, parent):
        self.state = state
        self.data_kind = "WMs"
        # headers = ["분류", "G-WM", "Item"]

        # Compose TreeView, Style Manager, and State Observer
        self.sheetview = BaseSheetView(parent, headers=None)
        self.state_observer = SheetViewStateObserver(
            state, self.sheetview, lambda e: self.update(state)
        )

        # Set up UI
        self.title_frame = ttk.Frame(parent)
        self.title_frame.pack(anchor="w")
        self.set_title(self.title_frame)
        self.sheetview.sheet.pack(expand=True, fill="both")
        self.sheetview.sheet.header_font(("Arial", 8, "normal"))
        self.sheetview.sheet.set_options(
            font=("Arial Narrow", 9, "normal"),
            default_row_height=30,
            # Bind selection events
        )  # Font name and size

        # Initialize the search manager
        self.search_manager = SheetSearchManager(self.sheetview.sheet, self.state)

        # Add Search Box
        self.add_search_box(self.title_frame)

        # action binding
        self.sheetview.sheet.extra_bindings(
            [
                (
                    "cell_select",
                    lambda e: self.on_cell_select(e, state, self.sheetview.sheet),
                ),
                (
                    "drag_select_cells",
                    lambda e: self.on_cell_select(e, state, self.sheetview.sheet),
                ),
            ]
        )

    def update(self, state):
        # Updating tksheet in the UI
        data_forSheet = state.team_std_info.get("WMs")
        sheetview_data = self.sheetview.sheet.get_sheet_data()
        # print(sheetview_data)
        if not sheetview_data:
            self.sheetview.sheet.set_sheet_data(data_forSheet)

    def add_search_box(self, parent):
        """Add search box to filter the sheet data."""
        search_frame = ttk.Frame(parent)
        search_frame.pack(padx=5, pady=5, anchor="w")

        # Search Label
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side="left", padx=5)

        # Search Entry
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind(
            "<Return>",
            lambda e: self.search_manager.search_sheet_data(self.search_entry.get()),
        )

        # Search Button
        search_button = ttk.Button(
            search_frame,
            text="Search",
            command=lambda: self.search_manager.search_sheet_data(
                self.search_entry.get()
            ),
        )
        search_button.pack(side="left", padx=5)

        # Reset Button
        reset_button = ttk.Button(
            search_frame,
            text="Reset",
            command=lambda: self.search_manager.reset_search(self.search_entry),
        )
        reset_button.pack(side="left", padx=5)

    def set_title(self, parent):
        self.widget_name = "WorkMaster DB"
        title_font = tk.font.Font(family="맑은 고딕", size=12)
        title_label = ttk.Label(parent, text=self.widget_name, font=title_font)
        title_label.pack(padx=5, pady=5, anchor="w")

    def on_cell_select(self, event, state, sheet, color="#fffec0"):
        # 선택된 셀의 위치 가져오기
        selected_cells = list(sheet.get_selected_cells())
        # state.selected_stdGWM_item.get().split(" | ")
        # grand_parent_item_name, parent_item_name, selected_item_name = (
        #     state.selected_stdGWM_item.get().split(" | ")
        # )
        if selected_cells:
            # 기존 스타일 초기화
            sheet.dehighlight_rows()

            # 선택된 행 강조 표시 (예: 노란색으로 설정)
            selected_rows = list(map(lambda x: x[0], selected_cells))
            # print(selected_rows)

            selectedWMs = []
            for row_idx in selected_rows:
                stringified_rowData = go(
                    sheet.get_row_data(row_idx),
                    map(lambda x: str(x)),
                    filter(lambda x: x != "0"),
                    filter(lambda x: x != ""),
                    filter(lambda x: x != " "),
                    filter(lambda x: x != "ㅤ"),  #  공백 특수 문자
                    lambda x: " | ".join(x),
                )
                selectedWMs.append(stringified_rowData)
            state.selectedWMs = selectedWMs
            # print(f"on_cell_select_WMsSheet: {selectedWMs}")
            sheet.highlight_rows(
                rows=selected_rows, bg=color, fg="black", highlight_index=True
            )

        # state.log_widget.write(
        #     f"선택 발생! 외애애애애애엥 [{self.widget_name}]시트, [{selected_cells}] 에서 선택 발생!!!!"
        # )


class ProjectApply_GWMSWM_Selcet_SheetView:
    def __init__(
        self, state, parent, relate_widget_std, related_widget_rvt, wm_mode="[ GWM ]"
    ):
        self.state = state
        self.data_kind = "project-assigntype"
        self.wm_mode = wm_mode
        self.treeDataManager = TreeDataManager_treesheet(state, self)
        self.relate_widget_std = relate_widget_std
        self.selected_item_relate_widget_std = relate_widget_std.selected_item
        self.related_widget_rvt = related_widget_rvt
        self.selected_item_relate_widget_rvt = related_widget_rvt.selected_item
        self.sheet = Sheet(
            parent,
            show_x_scrollbar=False,
            show_y_scrollbar=True,
            # show_header=False,
            # show_row_index=False,
            width=300,
            height=175,
        )
        self.sheet.pack(
            expand=True,
            # fill="both",
            # padx=5,
            # pady=5,
            anchor="w",
        )

        # config enable_bindings
        self.sheet.enable_bindings(
            "edit_cell",
            "delete",
            "single_select",  # Allow single cell selection
            "drag_select",
            "row_select",  # Allow row selection
            "column_select",  # Allow column selection
            "drag_select",  # Allow drag selection
            "column_width_resize",
            "row_height_resize",
            "double_click_column_resize",
            "copy",
            "paste",
            "ctrl_click_select",
            "right_click_popup_menu",
            "rc_insert_row",
            "rc_delete_row",
            "arrowkeys",
        )

        # Bind checkbox clicks
        self.sheet.extra_bindings(
            [
                ("end_edit_cell", lambda e: self.on_checkbox_click(e)),
            ]
        )

        # 초기 데이터 로드 및 시트 설정
        self.setup_sheet()

        # 상태 변경 감지를 위한 옵저버 설정
        self.state_observer = StateObserver(state, lambda e: self.update(e))

    def setup_sheet(self):
        # 헤더 설정
        headers = ["Use", "GWM/SWM", "Item"]
        self.sheet.headers(
            headers,
        )

        # Create checkboxes in the First column
        self.sheet.checkbox("A", checked=True)

        self.setup_column_style()
        # 초기 데이터 로드
        self.update()

    def setup_column_style(self):
        self.sheet.set_column_widths([25, 100, 100])

        self.sheet["A"].align("center")
        self.sheet.set_options(header_font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(font=("Arial", 10, "normal"))

        # self.sheet.set_options(default_row_height=40)

    def on_checkbox_click(self, event):
        """Callback for checkbox clicks."""
        self.state.log_widget.write(
            f"{self.__class__.__name__} > on_checkbox_click 메소드 시작"
        )
        selected_item_str = self.selected_item_relate_widget_std.get()
        project_GWM = self.state.team_std_info["project-GWM"].get(selected_item_str)

        # row = event["row"]
        # column = event["column"]
        # for r in range(self.sheet.get_total_rows()):
        #     if r != row:
        #         self.sheet.set_cell_data(r, 0, False)  # Uncheck other rows

        # # Ensure the clicked checkbox remains selected
        # self.sheet.set_cell_data(row, 0, True)

        # loc = list(event["cells"]["table"].keys())[0]
        # row_check_status = event["value"]

        # self.state.log_widget.write(f"위치: {loc}, 체크스테이터스 : {row_check_status}")

        # wm_code = self.sheet.get_cell_data(row, 3).split(" | ")[0]

        # if column == 0:
        #     if project_GWM:
        #         spec = project_GWM[-1]
        #         unit = project_GWM[-2]
        #     else:
        #         spec = go(
        #             self.sheet.get_cell_data(row, 3),
        #             lambda x: x.replace("\n", ""),
        #             lambda x: x.split(" | "),
        #             filter(lambda x: ("(   )" in x) or ("(   )" in x) or ("(  )" in x)),
        #             lambda x: "\n".join(x),
        #         )
        #     unit = go(
        #         self.sheet.get_cell_data(row, 3),
        #         lambda x: x.replace("\n", ""),
        #         lambda x: x.split(" | ")[-3],
        #     )
        # elif column == 1:
        #     spec = event["value"]
        #     unit = go(
        #         self.sheet.get_cell_data(row, 3),
        #         lambda x: x.replace("\n", ""),
        #         lambda x: x.split(" | ")[-3],
        #     )

        # # if row_check_status:
        # self.state.team_std_info["project-GWM"].update(
        #     {selected_item_str: [wm_code, unit, spec]}
        # )
        self.state.log_widget.write(
            self.state.team_std_info["project-GWM"][selected_item_str]
        )
        # self.highlight_checked_row()

    def highlight_checked_row(self):
        """Update row highlights based on checkbox values."""
        checked_rows = []
        for row in range(self.sheet.get_total_rows()):
            if self.sheet.get_cell_data(row, 0):  # If checkbox is checked
                checked_rows.append(row)

        # Clear existing highlights
        self.sheet.dehighlight_all()
        self.sheet.highlight_rows(
            checked_rows, highlight_index=False, bg="#D3F9D8"
        )  # Light green

    def wrap_text(self, text, width):
        """
        Wrap text to fit within a given width, handling long words properly.
        """
        if not text or not isinstance(text, str):
            return text
        max_chars_per_line = max(1, width // 7)  # Approximate character width in pixels

        words = text.split()  # Split into words
        lines = []
        current_line = ""

        for word in words:
            while len(word) > max_chars_per_line:  # Split long words into chunks
                lines.append(word[:max_chars_per_line])
                word = word[max_chars_per_line:]

            if len(current_line) + len(word) + 1 > max_chars_per_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = f"{current_line} {word}".strip()

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    def apply_wrap(self, tgt_idx, tgt_width=None):
        """
        Apply wrapping to all cells based on their column widths.
        """
        wrapped_data = []
        # for row_index, row in enumerate(self.sheet.get_sheet_data()):
        for row_index, row in enumerate(self.sheet.get_sheet_data()):
            wrapped_row = []
            for col_index, cell in enumerate(row):
                if col_index == tgt_idx:
                    if tgt_width:
                        width = tgt_width
                    else:
                        width = self.sheet.column_width(col_index)
                    wrapped_row.append(self.wrap_text(cell, width))
                else:
                    wrapped_row.append(cell)
            wrapped_data.append(wrapped_row)

        print(f"col width: {width}")
        # print(f"시트 data: {self.sheet.get_sheet_data()}")
        # print(f"시트 분할문자: {wrapped_data}")
        self.sheet.set_sheet_data(wrapped_data)

    def update(self, event=None):
        state = self.state
        """Update the TreeView whenever the state changes."""
        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")
        self.state.log_widget.write(
            f"선택아이템 출력 : {self.selected_item_relate_widget_std.get()}"
        )
        self.setup_column_style()

        existDatas = self.sheet.get_sheet_data()
        self.sheet.set_sheet_data([])
        for idx, value in enumerate(existDatas):
            self.sheet.del_dropdown(idx, 2)
        try:
            # Split the selected item path to find the grandparent, parent, and selected item names
            grand_parent_item_name, parent_item_name, selected_item_name = (
                self.selected_item_relate_widget_std.get().split(" | ")
            )

            # Ensure the data kind exists in the team standard information
            if "std-familylist" in state.team_std_info:
                data = state.team_std_info["std-familylist"]["children"]

                # Find the grandparent node
                grand_parent_node = next(
                    (node for node in data if node["name"] == grand_parent_item_name),
                    None,
                )
                if grand_parent_node:
                    # Find the parent node
                    parent_node = next(
                        (
                            node
                            for node in grand_parent_node["children"]
                            if node["name"] == parent_item_name
                        ),
                        None,
                    )
                    if parent_node:
                        # Find the selected node
                        selected_node = next(
                            (
                                node
                                for node in parent_node["children"]
                                if node["name"] == selected_item_name
                            ),
                            None,
                        )
                        if selected_node:
                            # Clear the TreeView and insert the data for the selected node
                            self.sheet.clear()

                            # Wrap the children of the selected node for insertion
                            # wrapped_data = go(
                            #     selected_node["children"],
                            #     filter(lambda x: x["values"][5] == self.wm_mode),
                            #     # map(lambda x: x["name"]),
                            #     map(
                            #         lambda x: [
                            #             "",
                            #             x["name"],
                            #             go(
                            #                 x,
                            #                 lambda y: list(
                            #                     map(lambda z: z["name"], y["children"])
                            #                 ),
                            #             ),
                            #         ]
                            #     ),
                            #     list,
                            # )

                            # wrapped_data = []
                            pool = go(
                                # deepcopy,
                                selected_node["children"],
                                filter(lambda x: x["values"][5] == self.wm_mode),
                                list,
                            )
                            wrapped_data = go(
                                pool,
                                map(lambda x: [False, x["name"], ""]),
                                list,
                            )

                            # self.sheet.set_data(
                            #     "A1",
                            #     [
                            #         ["", "A", "B", "C"],
                            #         ["1", "A1", "B1", "C1"],
                            #         ["2", "A2", "B2", "C2"],
                            #     ],
                            # )
                            # self.sheet.set_sheet_data(wrapped_data)
                            self.sheet.set_sheet_data([])
                            self.sheet.del_dropdown()

                            for idx, node in enumerate(pool):
                                self.sheet.insert_row(
                                    idx=idx,
                                    row=[True, node["name"], ""],
                                )

                                dropdown_values = go(
                                    node["children"],
                                    map(lambda x: x["name"]),
                                    list,
                                )
                                self.sheet.create_dropdown(
                                    idx, 2, values=dropdown_values
                                )

                            # print(f"\npool_data::: {pool}\n")

                            selected_item_str = (
                                self.selected_item_relate_widget_std.get()
                            )
                            # decided_WM = state.team_std_info["project-GWM"].get(
                            #     selected_item_str, None
                            # )

                            # tgt_rowIdx = 0
                            # if decided_WM:
                            #     for idx, row in enumerate(wrapped_data):
                            #         if decided_WM[0] in row[-1]:
                            #             row[0] = True
                            #             row[1] = decided_WM[-1]
                            #             row[2] = decided_WM[-2]
                            #             tgt_rowIdx = idx

                            # self.treeview.insert_data_with_levels(wrapped_data)
                            # self.sheet.set_sheet_data(wrapped_data)

                            # ###########test#################
                            # self.apply_wrap(tgt_idx=3, tgt_width=1000)
                            # self.sheet.set_all_cell_sizes_to_text()
                            # self.sheet.set_all_row_heights(
                            #     height=50,
                            #     only_set_if_too_small=True,
                            # )
                            # ###########test#################

                            # self.sheet.see(tgt_rowIdx, 0)
                        else:
                            self.state.log_widget.write(
                                f"Selected item '{selected_item_name}' not found."
                            )
                    else:
                        self.state.log_widget.write(
                            f"Parent item '{parent_item_name}' not found."
                        )
                else:
                    self.state.log_widget.write(
                        f"Grandparent item '{grand_parent_item_name}' not found."
                    )

        except Exception as e:
            self.state.log_widget.write(
                f"{self.__class__.__name__} > update 메소드 진입 안됩니다~: {e}"
            )

        self.setup_column_style()
        self.highlight_checked_row()

        self.state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")

    def set_edit_mode(self, mode):
        # 편집 모드 설정
        if mode == "edit":
            self.sheet.enable_bindings()
        else:
            self.sheet.disable_bindings()


class TreeviewSheet:
    def __init__(self, parent, headers):
        self.sheet = Sheet(parent, headers=headers)
        self.parent = parent

        # config enable_bindings
        self.sheet.enable_bindings(
            "edit_cell",
            "delete",
            "single_select",  # Allow single cell selection
            "drag_select",
            "row_select",  # Allow row selection
            "column_select",  # Allow column selection
            "drag_select",  # Allow drag selection
            "column_width_resize",
            "row_height_resize",
            "double_click_column_resize",
            "copy",
            "paste",
            "ctrl_click_select",
            "right_click_popup_menu",
            "rc_insert_row",
            "rc_delete_row",
            "arrowkeys",
        )

    def insert_data(self, item, parent=None):
        pass

    def clear_sheet(self):
        pass

    def get_sheet_data(self):
        pass

    def toggle_sheet_lock(self, lock=True):
        pass

    def collapse_all_items(self):
        pass

    def expand_all_items(self):
        pass

    def expand_tree_to_level(self, level):
        pass

    def insert_data_with_levels(self, data, parents_id=""):
        pass

    def get_item_indices(self, selected_item_id):
        pass

    def select_item_by_indices(self, indices):
        pass

    ####
