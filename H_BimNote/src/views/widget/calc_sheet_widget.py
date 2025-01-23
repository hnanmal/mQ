import tkinter as tk
from tkinter import ttk
from tksheet import Sheet, num2alpha as n2a
import openpyxl

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.views.widget.widget import StateObserver

# from src.views.widget.sheet_utils import SheetSearchManager


class SearchManager:
    def __init__(self, parent_frame, sheet_widget):
        """
        Initialize the SearchManager.
        :param parent_frame: The parent frame where the search UI components will be added.
        :param sheet_widget: The tksheet widget to which search functionality will be applied.
        """
        self.sheet = sheet_widget
        self.parent_frame = parent_frame

        # Create search UI components
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            parent_frame, textvariable=self.search_var, width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = ttk.Button(
            parent_frame, text="Search", command=self.search_sheet
        )
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(
            parent_frame, text="Clear Search", command=self.clear_search
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.noti_label = ttk.Label(
            parent_frame,
            text="Dynamo 에서 물량 산출을 하기 전, 반드시 B-note의 현재 상태를 저장해 주세요!",
            font=("맑은고딕", 14, "bold"),
            foreground="red",
        )
        self.noti_label.pack(side=tk.LEFT, padx=5)

        # Bind Enter key to search functionality
        self.search_entry.bind("<Return>", lambda event: self.search_sheet())

    def search_sheet(self):
        """Search for rows containing the search term."""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.sheet.display_rows("all")  # Show all rows if search is empty
            self.sheet.redraw()  # Refresh the sheet immediately
            return

        sheet_data = self.sheet.get_sheet_data()
        matching_rows = [
            rn
            for rn, row in enumerate(sheet_data)
            if any(search_term in str(cell).lower() for cell in row)
        ]

        self.sheet.display_rows(rows=matching_rows, all_displayed=False)
        self.sheet.redraw()  # Refresh the sheet immediately
        print(f"Search term '{search_term}' found in rows: {matching_rows}")

    def clear_search(self):
        """Clear the search field and reset the displayed rows."""
        self.search_var.set("")
        self.sheet.display_rows("all")
        self.sheet.redraw()  # Refresh the sheet immediately


class ReportSheetWidget(ttk.Frame):
    def __init__(self, state, parent, data_kind=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.state = state
        self.data_kind = data_kind
        self.data = []
        self.column_headers = []

        # Load data
        self.load_data()

        # Create a frame for the top controls (button)
        self.control_frame = ttk.Frame(parent)
        self.control_frame.pack(fill=tk.X, pady=5)

        # Add "Clear Filters" button at the top
        self.clear_button = ttk.Button(
            self.control_frame, text="Clear Filters", command=self.clear_filters
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Initialize tksheet widget
        self.sheet = Sheet(
            self,
            data=self.data,
            column_width=180,
            # theme="dark",
            # theme="light green",
            height=500,
            width=1000,
        )
        self.sheet.enable_bindings(
            "copy",
            "rc_select",
            "arrowkeys",
            "double_click_column_resize",
            "column_width_resize",
            "column_select",
            "row_select",
            "drag_select",
            "single_select",
            "select_all",
        )

        self.sheet.set_options(header_font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(font=("Arial Narrow", 8, "normal"))
        self.sheet.set_options(set_all_heights_and_widths=True)
        self.set_colums_widths()
        # self.sheet.set_all_cell_sizes_to_text()

        self.sheet.pack(fill=tk.BOTH, expand=True)

        # Add header dropdowns
        self.add_dropdowns()

        # Add search functionality
        self.search_manager = SearchManager(self.control_frame, self.sheet)

        # 상태 변경 감지를 위한 옵저버 설정
        self.state_observer = StateObserver(state, lambda e: self.update(e))

    def set_colums_widths(self, hdr_widths=None):
        # self.sheet.headers(self.column_headers)
        if hdr_widths:
            self.sheet.set_column_widths(hdr_widths)
        else:
            self.sheet.set_column_widths(
                [
                    60,  # 카테고리
                    70,  # 표준타입번호
                    140,  # 표준타입
                    50,  # 분류
                    200,  # name
                    150,  # GUID
                    180,  # 상세분류
                    100,  # wm_code
                    50,  # gauge
                    150,  # description
                    540,  # Spec.
                    180,  # Add_spec.
                    150,  # 수식
                    200,  # 대입수식
                    50,  # 산출결과
                    50,  # 단위
                    50,  # 산출유형
                    200,  # 산출로그
                ]
            )

    def update(self, event=None):
        """Update the Sheet widget whenever the state changes."""
        state = self.state
        state.log_widget.write(f"{self.__class__.__name__} > update 메소드 시작")
        print(f"{self.__class__.__name__} > update 메소드 시작")

        # Reload data
        self.load_data()

        # Set headers and data
        self.sheet.set_sheet_data(
            self.data, reset_col_positions=True, reset_row_positions=True
        )
        self.sheet.headers(self.column_headers)

        # Reinitialize dropdowns
        self.add_dropdowns()

        self.clear_filters()

        # Ensure cell sizes and redraw
        # self.sheet.set_all_cell_sizes_to_text()
        self.set_colums_widths()
        self.sheet.redraw()

        state.log_widget.write(f"{self.__class__.__name__} > update 메소드 종료")
        print(f"{self.__class__.__name__} > update 메소드 종료")

    def load_data(self):
        state = self.state
        """Load data from Excel file and set headers and data."""
        try:
            # workbook = openpyxl.load_workbook(self.excel_file, data_only=True)
            # sheet = workbook.active
            data = self.data
            # Extract headers
            src_data = state.team_std_info[self.data_kind].get(
                state.current_building.get()
            )
            self.column_headers = src_data[0]
            # self.sheet.headers(self.column_headers)

            # Extract data
            self.data = src_data[1:]
            # self.data = src_data

            # self.sheet.set_sheet_data(self.data)
            print("ok~")
        except Exception as e:
            # self.sheet.set_sheet_data([])
            self.data = []
            print(f"Error loading data: {e}")

    def add_dropdowns(self, target_col_index=None):
        """Add dropdowns dynamically to each header based on the displayed rows."""
        current_headers = self.sheet.headers()  # Get current header values
        displayed_data = self.sheet.get_sheet_data(
            get_displayed=True
        )  # Get only displayed rows
        # print(f"Displayed data for dropdown update: {displayed_data}")  # Debugging

        if target_col_index is not None:
            # Update only the dropdown for the selected column
            header = self.column_headers[target_col_index]
            unique_values = ["all"] + sorted(
                set(
                    row[target_col_index]
                    for row in displayed_data
                    if row[target_col_index] is not None
                )
            )
            print(
                f"Updating dropdown for column {header} with values: {unique_values}"
            )  # Debugging
            current_value = (
                current_headers[target_col_index]
                if target_col_index < len(current_headers)
                else "all"
            )
            self.sheet.dropdown(
                self.sheet.span(n2a(target_col_index), header=True, table=False),
                values=unique_values,
                set_value=current_value,
                selection_function=lambda event, col=target_col_index: self.header_dropdown_selected(
                    event, col
                ),
                text=header,
            )
        else:
            # Update all dropdowns (initial setup or full refresh)
            for col_idx, header in enumerate(self.column_headers):
                unique_values = ["all"] + sorted(
                    set(
                        row[col_idx]
                        for row in displayed_data
                        if row[col_idx] is not None
                    )
                )
                # print(
                #     f"Updating dropdown for column {header} with values: {unique_values}"
                # )  # Debugging
                current_value = (
                    current_headers[col_idx]
                    if col_idx < len(current_headers)
                    else "all"
                )
                self.sheet.dropdown(
                    self.sheet.span(n2a(col_idx), header=True, table=False),
                    values=unique_values,
                    set_value=current_value,
                    selection_function=lambda event, col=col_idx: self.header_dropdown_selected(
                        event, col
                    ),
                    text=header,
                )

    def header_dropdown_selected(self, event, col_index):
        """Filter rows based on header dropdown selection."""
        hdrs = self.sheet.headers()
        hdrs[event.loc] = event.value

        if all(dd == "all" for dd in hdrs):  # No filters applied
            self.sheet.display_rows("all")
        else:  # Apply filters
            rows = [
                rn
                for rn, row in enumerate(self.data)
                if all(row[c] == e or e == "all" for c, e in enumerate(hdrs))
            ]
            self.sheet.display_rows(rows=rows, all_displayed=False)
            # self.sheet.display_rows(rows=rows, all_rows_displayed=False)
            self.add_dropdowns()
            self.sheet.redraw()

        # Recompute only the affected dropdown
        # self.add_dropdowns()
        # Redraw only once
        self.set_colums_widths()
        self.sheet.redraw()

    def clear_filters(self):
        """Clear all filters and reset the table to show all data."""
        # Reset all headers to "all"
        hdrs = ["all"] * len(self.column_headers)
        self.sheet.headers(hdrs)

        # Display all rows
        self.sheet.display_rows(
            "all", reset_col_positions=True, reset_row_positions=True
        )

        # Recompute dropdown options based on the full dataset
        self.add_dropdowns()

        # Ensure everything is redrawn
        self.set_colums_widths()
        self.sheet.redraw()


# # Example usage
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Excel Data Viewer with Filters")
#     root.geometry("1200x600")

#     # Replace with your Excel file path
#     excel_file_path = "SACE2__excel_qty_result_0121-022123.xlsx"

#     # Create and pack the ExcelSheetWidget
#     excel_widget = ExcelSheetWidget(root, excel_file_path)
#     excel_widget.pack(fill=tk.BOTH, expand=True)

#     root.mainloop()
