import tkinter as tk
from tksheet import Sheet


class FinishMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("인테리어 피니시 매트릭스")

        # ✅ 대분류(Materials) + 하위 항목(Sub-Materials) 데이터 구조
        self.materials = {
            "Floor": [
                "Hardener",
                "Mat",
                "N.A",
                "Paint",
                "Paint::Acid",
                "Paint::Acrylic",
                "Paint::Anti Dust",
                "Paint::Chemical",
                "Paint::Epoxy",
                "Raised Floor",
                "Raised Floor::1000",
                "Raised Floor::700",
                "Screed",
                "Tile",
                "Tile:: Non-Slip Ceramic ",
                "Tile::Acid",
                "Tile::Carpet",
                "Tile::Vinyl",
                "Tile::Wood",
                "Trowel",
                "Waterproofing",
                "Waterproofing:: Liquid",
                "Waterproofing:: Polyurethane",
            ],
            "Skirt": [
                "AL Baseboard",
                "Hard Wood Trim",
                "N.A",
                "Paint",
                "Paint::Acrylic",
                "Paint::EP-100",
                "Paint::EP-700",
                "Rubber",
                "Tile::AT",
                "Tile::UC",
                "Tile::VT_100",
                "Tile::VT_200",
            ],
            "Wall": [
                "N.A",
                "Paint",
                "Paint:: Acrylic Emulsion",
                "Paint:: Chemical",
                "Paint::Acid",
                "Plaster",
                "Plaster:: 18mm",
                "Plaster:: 21mm",
                "Plywood",
                "Sound Absorbing",
                "Tile",
                "Tile:: Glazed Ceramic",
                "Tile::UG",
                "Waterproofing",
                "Waterproofing:: Liquid",
                "Waterproofing:: Membrane",
            ],
            "Ceiling": [
                "Gypsum board ",
                "Insulation",
                "Paint",
                "Paint:: Acid",
                "Paint:: Acrylic Emulsion",
                "Sound Abs",
                "Suspended Ceiling",
                "Suspended Ceiling:: Acoustic T-Bar",
                "Suspended Ceiling::AL_Mbar",
                "Suspended Ceiling::Mineral Board",
                "Suspended Ceiling::Moisture",
            ],
        }

        # ✅ 룸 목록 (열)
        self.all_rooms = [
            "Room A",
            "Room B",
            "Room C",
            "Room D",
            "Room E",
            "Room F",
            "Room G",
            "Room H",
            "Room I",
            "Room J",
            "Room K",
            "Room L",
            "Room M",
            "Room N",
            "Room O",
        ]

        # ✅ 현재 표시할 룸 목록 (필터 적용 가능)
        self.filtered_rooms = self.all_rooms[:]

        # ✅ 체크 상태 저장 (Dictionary)
        self.check_status = {
            room: {
                mat: False
                for category in self.materials
                for mat in self.materials[category]
            }
            for room in self.all_rooms
        }

        # ✅ 검색 필터 입력창
        self.filter_var = tk.StringVar()
        self.filter_entry = tk.Entry(self.root, textvariable=self.filter_var, width=20)
        self.filter_entry.pack(pady=5)
        self.filter_button = tk.Button(
            self.root, text="필터 적용", command=self.apply_filter
        )
        self.filter_button.pack(pady=5)

        # ✅ 테이블을 위한 행 구성 (대분류 & 하위 항목)
        self.material_rows = []
        self.category_rows = set()  # ✅ 대분류 행 인덱스를 저장
        row_index = 0

        for category, sub_materials in self.materials.items():
            self.material_rows.append(category)  # ✅ 대분류 (체크 불가)
            self.category_rows.add(row_index)  # ✅ 대분류 행 인덱스 저장
            row_index += 1
            self.material_rows.extend(sub_materials)  # ✅ 하위 항목 (체크 가능)
            row_index += len(sub_materials)

        # ✅ tksheet 생성 (가로 스크롤 지원)
        self.sheet = Sheet(
            self.root,
            data=[
                [""] * len(self.filtered_rooms) for _ in range(len(self.material_rows))
            ],
            headers=self.filtered_rooms,
            row_index=self.material_rows,
            align="c",
        )

        self.sheet.enable_bindings()
        self.sheet.pack(fill="both", expand=True)

        # ✅ 폰트 크기 조정 (튜플 형식 수정)
        self.sheet.set_options(editable=True, font=("Arial", 12, "normal"))

        # ✅ 스타일 적용 (대분류 행)
        self.apply_styles()

        # ✅ 클릭 이벤트 바인딩 (셀 클릭 시 체크박스 토글)
        # self.sheet.extra_bindings("cell_select", self.toggle_checkbox)
        self.sheet.extra_bindings("begin_edit_cell", self.toggle_checkbox)

        # ✅ 더블클릭 비활성화

        # self.sheet.extra_bindings("cell_double_click", lambda e: break_func)
        # self.sheet.disable_bindings("edit_cell")

    def apply_styles(self):
        """✅ 대분류(Materials) 스타일 적용: 글자색 회색, 배경 보라색"""
        for row_idx in self.category_rows:
            self.sheet.highlight_rows(
                row_idx, bg="#D8BFD8", fg="gray"
            )  # ✅ 연한 보라색 배경, 회색 글자 (underline 제거)

    def toggle_checkbox(self, event):
        """✅ 셀 클릭 시 체크박스를 토글하는 함수"""
        selected_cells = list(
            self.sheet.get_selected_cells()
        )  # ✅ 'set'을 리스트로 변환
        if not selected_cells:
            return

        row, col = selected_cells[0]
        material_name = self.material_rows[row]  # ✅ 원래 데이터 가져오기
        room = self.filtered_rooms[col]

        # ✅ 대분류(바닥, 천장, 걸레받이, 벽)는 체크 불가능
        if row in self.category_rows:
            return

        # ✅ 현재 상태 반전 (체크/해제)
        self.check_status[room][material_name] = not self.check_status[room][
            material_name
        ]

        # ✅ 체크된 상태에 따라 셀 내용 업데이트
        self.sheet.set_cell_data(
            row, col, "✅" if self.check_status[room][material_name] else ""
        )

        # ✅ 마감 사양 데이터 업데이트
        self.update_finish_data(room)

    def update_finish_data(self, room):
        """✅ 특정 룸(Room)에 대한 마감 사양을 업데이트하는 함수"""
        selected_materials = [
            mat for mat, checked in self.check_status[room].items() if checked
        ]
        print(f"{room}의 마감 사양: {', '.join(selected_materials)}")

    def apply_filter(self):
        """✅ 검색 필터 적용"""
        search_text = self.filter_var.get().strip().lower()

        if search_text:
            self.filtered_rooms = [
                room for room in self.all_rooms if search_text in room.lower()
            ]
        else:
            self.filtered_rooms = self.all_rooms[:]

        # ✅ 필터 적용 후 테이블 업데이트
        self.update_table()

    def update_table(self):
        """✅ 필터 적용 후 tksheet 업데이트"""
        self.sheet.headers(self.filtered_rooms)  # ✅ 헤더 업데이트

        # ✅ 기존 체크 상태 반영
        new_data = []
        for row_idx, row_name in enumerate(self.material_rows):
            if row_idx in self.category_rows:
                new_data.append(
                    [""] * len(self.filtered_rooms)
                )  # ✅ 대분류 행은 체크 없음
            else:
                row_data = [
                    "✅" if self.check_status[room][row_name] else ""
                    for room in self.filtered_rooms
                ]
                new_data.append(row_data)

        self.sheet.set_sheet_data(new_data)  # ✅ 데이터 업데이트
        self.sheet.redraw()  # ✅ 화면 갱신

        # ✅ 스타일 다시 적용
        self.apply_styles()


# ✅ Tkinter 실행
root = tk.Tk()
app = FinishMatrixApp(root)
root.mainloop()
