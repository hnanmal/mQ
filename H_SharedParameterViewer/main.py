import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkbootstrap import Style
from tksheet import Sheet
from tkinterdnd2 import DND_FILES, TkinterDnD


class SharedParameterViewer(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.group_map = {}
        self.param_data_raw = []
        self.sort_state = {}

        # ───────── 상단 툴바 ─────────
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        btn = ttk.Button(
            top_frame,
            text="Open SharedParameter.txt",
            command=self.load_file,
            bootstyle="primary-outline",
        )
        btn.pack(side="left", padx=(0, 10))

        tk.Label(top_frame, text="Filter by Group:").pack(side="left", padx=(0, 5))
        self.group_combo = ttk.Combobox(top_frame, state="readonly", width=30)
        self.group_combo.pack(side="left")
        self.group_combo.bind(
            "<<ComboboxSelected>>",
            lambda e: self.filter_and_display(self.group_combo.get()),
        )

        tk.Label(top_frame, text="Search:").pack(side="left", padx=(20, 5))
        self.search_entry = tk.Entry(top_frame, width=30)
        self.search_entry.pack(side="left", padx=(0, 5))
        self.search_entry.bind("<Return>", lambda e: self.apply_search())

        search_btn = tk.Button(top_frame, text="Search", command=self.apply_search)
        search_btn.pack(side="left")

        tk.Label(top_frame, text="Sort by:").pack(side="left", padx=(20, 5))
        self.sort_combo = ttk.Combobox(top_frame, state="readonly", width=20)
        self.sort_combo.pack(side="left", padx=(0, 5))

        sort_btn = ttk.Button(
            top_frame,
            text="Sort\n(단축키 S)",
            command=self.sort_by_selected_column,
            bootstyle="info",
        )
        sort_btn.pack(side="left", padx=(0, 10))

        # ───────── 시트 영역 ─────────
        sheet_frame = tk.Frame(self)
        sheet_frame.pack(fill="both", expand=True)

        self.sheet = Sheet(sheet_frame)
        self.sheet.enable_bindings(
            (
                "single_select",
                "column_select",
                "row_select",
                "copy",
                "paste",
                "column_width_resize",
                "double_click_column_resize",
            )
        )
        self.sheet.set_options(
            font=("맑은 고딕", 9, "normal"), header_font=("맑은 고딕", 8, "normal")
        )
        self.sheet.pack(fill="both", expand=True)

        # ✅ 단축키: s 하나로 정렬
        self.bind_all("<Key-s>", self.handle_sort_key)
        self.bind_all("<Key-S>", self.handle_sort_key)

        # ✅ 드래그 앤 드롭 활성화
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.on_file_drop)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])
        if path:
            self.load_file_from_path(path)

    def load_file_from_path(self, path):
        headers = self.parse_file(path)
        if not headers:
            return

        self.sheet.headers(headers)
        self.sort_combo["values"] = headers
        self.sort_combo.current(1)

        group_list = ["All"] + sorted(set(self.group_map.values()))
        self.group_combo["values"] = group_list
        self.group_combo.current(0)
        self.filter_and_display("All")

    def on_file_drop(self, event):
        path = event.data.strip().strip("{}")  # 경로 포맷 정리
        if path.lower().endswith(".txt"):
            self.load_file_from_path(path)
        else:
            messagebox.showwarning(
                "형식 오류", "지원하는 SharedParameter.txt 파일만 가능합니다."
            )

    def parse_file(self, filepath):
        self.group_map.clear()
        self.param_data_raw.clear()

        try:
            with open(filepath, "r", encoding="utf-16") as f:
                lines = f.readlines()
        except Exception as e:
            messagebox.showerror("파일 열기 오류", f"파일을 열 수 없습니다:\n{e}")
            return []

        if not self.is_valid_shared_parameter(lines):
            messagebox.showerror(
                "파일 형식 오류", "선택한 파일은 Revit SharedParameter 형식이 아닙니다."
            )
            return []

        headers = [
            "GUID",
            "NAME",
            "DATATYPE",
            "DATACATEGORY",
            "GROUP",
            "VISIBLE",
            "DESCRIPTION",
            "USERMODIFIABLE",
            "HIDEWHENNOVALUE",
        ]

        try:
            for line in lines:
                parts = line.strip().split("\t")
                if parts[0] == "GROUP":
                    self.group_map[parts[1]] = parts[2]
                elif parts[0] == "PARAM":
                    parts = parts[1:]
                    if len(parts) < 9:
                        parts += [""] * (9 - len(parts))
                    group_id = parts[4]
                    group_name = self.group_map.get(group_id, group_id)
                    visible = "Yes" if parts[5] == "1" else "No"
                    usermod = "Yes" if parts[7] == "1" else "No"
                    hidewhenno = "Yes" if parts[8] == "1" else "No"
                    self.param_data_raw.append(
                        [
                            parts[0],
                            parts[1],
                            parts[2],
                            parts[3],
                            group_name,
                            visible,
                            parts[6],
                            usermod,
                            hidewhenno,
                        ]
                    )
        except Exception as e:
            messagebox.showerror(
                "파싱 오류", f"파일을 처리하는 중 오류가 발생했습니다.\n\n{e}"
            )
            return []

        return headers

    def is_valid_shared_parameter(self, lines):
        return (
            any("*META" in line for line in lines)
            and any("*GROUP" in line for line in lines)
            and any("*PARAM" in line for line in lines)
        )

    def filter_and_display(self, selected_group):
        if selected_group == "All":
            filtered = self.param_data_raw
        else:
            filtered = [row for row in self.param_data_raw if row[4] == selected_group]

        self.sheet.set_sheet_data(filtered, reset_col_positions=True)
        self.after(100, self.auto_resize_columns)
        self.after(110, self.apply_search)

    def auto_resize_columns(self):
        for col_index in range(self.sheet.total_columns()):
            self.sheet.column_width(
                col_index, width="text", only_set_if_too_small=False
            )

        self.sheet.highlight_columns(
            columns=[0], fg="#888888", redraw=True
        )  # GUID 칼럼

    def apply_search(self):
        keyword = self.search_entry.get().lower().strip()
        self.sheet.dehighlight_all()
        self.sheet.highlight_columns(columns=[0], fg="#888888", redraw=True)

        if not keyword:
            return

        matches = []
        for i, row in enumerate(self.sheet.get_sheet_data()):
            for cell in row:
                if keyword in str(cell).lower():
                    matches.append(i)
                    break

        if matches:
            self.sheet.highlight_rows(
                rows=matches, bg="lightyellow", fg="black", redraw=True
            )
            self.sheet.highlight_columns(columns=[0], fg="#888888", redraw=True)

    def sort_by_selected_column(self):
        col_name = self.sort_combo.get()
        if not col_name:
            return

        try:
            col_index = self.sheet.headers().index(col_name)
        except ValueError:
            return

        ascending = self.sort_state.get(col_index, True)
        self.sort_state[col_index] = not ascending

        current_data = self.sheet.get_sheet_data()
        sorted_data = sorted(
            current_data,
            key=lambda row: str(row[col_index]).lower(),
            reverse=not ascending,
        )
        self.sheet.set_sheet_data(sorted_data, reset_col_positions=True)
        self.after(100, self.auto_resize_columns)
        self.after(110, self.apply_search)

    def handle_sort_key(self, event):
        if self.focus_get() == self.search_entry:
            return
        self.sort_by_selected_column()


if __name__ == "__main__":
    import os
    import tkinterdnd2

    # 드래그앤드롭 DLL 경로 설정 (PyInstaller 패키지 후에도 동작)
    tkdnd_path = os.path.join(os.path.dirname(__file__), "tkinterdnd2", "tkdnd2.9")
    os.environ["TKDND_LIBRARY_PATH"] = tkdnd_path

    root = TkinterDnD.Tk()
    root.title("Revit Shared Parameter Viewer")
    root.geometry("1200x700")
    Style("minty")

    viewer = SharedParameterViewer(root)
    viewer.pack(fill="both", expand=True)

    root.mainloop()
