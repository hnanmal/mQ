from src.controllers.tree_data_navigator import TreeDataManager_treesheet
from src.core.fp_utils import *
import tkinter as tk
import tkinter.font
from tksheet import Sheet

# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from src.views.widget.widget import StateObserver


class pjt_interior_matrix_widget:
    def __init__(self, state, parent):
        self.state = state
        self.data_kind = "project-assigntype"
        self.treeDataManager = TreeDataManager_treesheet(state, self)
        self.state_observer = StateObserver(state, lambda e: self.update(e))

        # ✅ 대분류(Materials) + 하위 항목(Sub-Materials) 데이터 구조
        self.materials = {}

        # ✅ 룸 목록 (열)
        self.all_rooms = []

        # ✅ 현재 표시할 룸 목록 (필터 적용 가능)
        self.filtered_rooms = self.all_rooms[:]

        self.material_rows = []
        self.category_rows = set()  # ✅ 대분류 행 인덱스를 저장

        self.combobox_area = ttk.Frame(parent)
        self.combobox_area.pack(anchor="nw", fill="x")
        self.sheet_area = ttk.Frame(parent)
        self.sheet_area.pack(anchor="nw", fill="both", expand=True)

        self.select_lv_label = ttk.Label(
            self.combobox_area,
            text="층을 선택해주세요 >>",
        )
        self.select_lv_label.pack(side="left")
        self.fl_combo = ttk.Combobox(self.combobox_area, values=[])
        self.fl_combo.pack(side="left")
        # Bind the <<ComboboxSelected>> event to the handler
        self.fl_combo.bind(
            "<<ComboboxSelected>>", lambda event: self.on_combobox_select(event, state)
        )

        # ✅ tksheet 생성 (가로 스크롤 지원)
        self.sheet = Sheet(
            self.sheet_area,
            data=[],
            # default_header=[],
            # headers=self.filtered_rooms,
            # row_index=self.material_rows,
            align="c",
        )
        self.sheet.set_index_width(200)
        self.sheet.enable_bindings()
        self.sheet.pack(fill="both", expand=True)

        # ✅ 클릭 이벤트 바인딩 (셀 클릭 시 체크박스 토글)
        self.sheet.extra_bindings("begin_edit_cell", self.toggle_checkbox)

    def setup_sheet(self, headers):
        # 헤더 설정

        self.sheet.headers(
            headers,
        )
        # self.setup_column_style()

        # self.sheet.set_sheet_data([])

    def get_level_fromRoomName(self, name):
        res = go(
            name,
            lambda x: x.split("_"),
            lambda x: x[0][0],
        )
        return res

    def set_floor_commbovalues(self):
        state = self.state
        if state.current_building:
            floors = go(
                self.all_rooms,
                map(self.get_level_fromRoomName),
                set,
                list,
                sorted,
            )
            print(f"[int matrix] floors : {floors}")
        else:
            floors = ["건물선택필요"]

        self.fl_combo.config(values=floors)
        # self.fl_combo.set(floors[0])

    def set_row_idx(self):
        # ✅ 테이블을 위한 행 구성 (대분류 & 하위 항목)
        self.material_rows = []
        self.category_rows = set()  # ✅ 대분류 행 인덱스를 저장
        row_index = 0

        for category, sub_materials in self.materials.items():
            # for category, sub_materials in sorted(self.materials.items()):
            self.material_rows.append(category)  # ✅ 대분류 (체크 불가)
            self.category_rows.add(row_index)  # ✅ 대분류 행 인덱스 저장
            row_index += 1
            self.material_rows.extend(sorted(sub_materials))  # ✅ 하위 항목 (체크 가능)
            row_index += len(sub_materials)

        self.sheet.row_index(self.material_rows)

    def apply_styles(self):
        # ✅ 폰트 크기 조정 (튜플 형식 수정)
        self.sheet.set_options(editable=True, font=("Arial", 12, "normal"))

        """✅ 대분류(Materials) 스타일 적용: 글자색 회색, 배경 보라색"""
        for row_idx in self.category_rows:
            self.sheet.highlight_rows(
                row_idx, bg="#D8BFD8", fg="gray"
            )  # ✅ 연한 보라색 배경, 회색 글자 (underline 제거)

    # Event handler for combo box selection
    def on_combobox_select(self, event, state):
        selected_value = event.widget.get()  # Get the selected value from the combo box
        self.set_floor_commbovalues()

        state.observer_manager.notify_observers(state)

    def update(self, event=None):
        state = self.state
        self.sheet.set_sheet_data([])
        # self.sheet.set_header_data([])
        # ✅ 필터 적용 후 tksheet 업데이트
        # self.sheet.headers([])  # ✅ 헤더 초기화

        std_data = state.team_std_info.get("std-familylist")
        pjt_data = state.team_std_info.get(self.data_kind)
        # self.filtered_rooms = []
        SWM = go(
            std_data["children"][0]["children"],
            filter(lambda x: x["name"] == "0.Room"),
            lambda x: list(x)[0]["children"],
            filter(lambda x: x["name"] == "0.1"),
            lambda x: list(x)[0]["children"],
            list,
        )

        SWM_names = go(
            SWM,
            map(lambda x: x["name"]),
            list,
        )
        SWMitem_names = go(
            SWM,
            map(lambda x: x["children"]),
            map(lambda x: list(map(lambda y: y["name"], x))),
            list,
        )

        self.materials = dict(zip(SWM_names, SWMitem_names))

        print(f"[int matrix] self.materials : {self.materials}")
        # self.sheet.set_sheet_data([])
        # self.setup_column_style()

        rooms_for_selectedBuilding = go(
            pjt_data["children"],
            filter(lambda x: x["values"][1] == state.current_building.get()),
            filter(lambda x: x["values"][-1] == "Top | 0.Room | 0.1"),
            map(lambda x: x["name"]),
            map(lambda x: x.replace("\t", "_")),
            list,
        )
        self.all_rooms = rooms_for_selectedBuilding
        # ✅ 레벨 콤보박스 업데이트
        self.set_floor_commbovalues()

        selected_lv = self.fl_combo.get()

        rooms_for_selectedLevel = go(
            rooms_for_selectedBuilding,
            filter(lambda x: self.get_level_fromRoomName(x) == selected_lv),
            list,
        )
        self.filtered_rooms = rooms_for_selectedLevel
        print(f"[int matrix] rooms_for_selectedBuilding : {rooms_for_selectedLevel}")

        # self.sheet.set_sheet_data([])  # ✅ 헤더 업데이트
        # self.sheet.headers(self.filtered_rooms)  # ✅ 헤더 업데이트
        self.sheet.pack_forget()
        self.sheet = Sheet(
            self.sheet_area,
            data=[],
            headers=self.filtered_rooms,
            row_index=self.material_rows,
            align="c",
        )
        self.sheet.enable_bindings()
        self.sheet.pack(fill="both", expand=True)

        # ✅ 클릭 이벤트 바인딩 (셀 클릭 시 체크박스 토글)
        self.sheet.extra_bindings("begin_edit_cell", self.toggle_checkbox)

        # ✅ 테이블을 위한 행 구성 (대분류 & 하위 항목)
        self.set_row_idx()
        self.sheet.set_index_width(200)

        # ✅ DB 체크 상태 반영
        def get_db_status_forRoom(room, row_idx):
            col = self.filtered_rooms.index(room)

            roomName_asDBformat = room.replace("_", "\t")

            tgt_room_db = go(
                state.team_std_info[self.data_kind]["children"],
                filter(lambda x: x["name"] == roomName_asDBformat),
                next,
                lambda x: x["children"],
            )
            tgt_room_material_names = go(
                tgt_room_db,
                map(lambda x: x[2]),
                list,
            )
            SWM_names = [
                "Floor",
                "Skirt",
                "Wall",
                "Ceiling",
            ]

            SWM_idxes = [self.material_rows.index(x) for x in SWM_names]

            row_dist = [x - row_idx for x in SWM_idxes]
            min_row_dist = go(
                row_dist,
                filter(lambda x: x < 0),
                max,
            )
            parent_SWM_idx = row_dist.index(min_row_dist)
            SWM_name = SWM_names[parent_SWM_idx]

            material_name = self.material_rows[row_idx]  # ✅ 원래 데이터 가져오기
            material_full_name = " | ".join([SWM_name, material_name])

            res = material_full_name in tgt_room_material_names
            return res

        new_data = []
        for row_idx, row_name in enumerate(self.material_rows):
            if row_idx in self.category_rows:
                new_data.append(
                    [""] * len(self.filtered_rooms)
                )  # ✅ 대분류 행은 체크 없음
            else:
                row_data = [
                    "✅" if get_db_status_forRoom(room, row_idx) else ""
                    for room in self.filtered_rooms
                ]
                # row_data = [
                #     "✅" if self.check_status[room][row_name] else ""
                #     for room in self.filtered_rooms
                # ]
                new_data.append(row_data)
        print(f"new_data {new_data}")

        self.sheet.set_sheet_data(new_data)  # ✅ 데이터 업데이트
        self.sheet.redraw()  # ✅ 화면 갱신

        # ✅ 스타일 다시 적용
        self.apply_styles()

    def toggle_checkbox(self, event):
        """✅ 셀 클릭 시 체크박스를 토글하는 함수"""
        state = self.state
        selected_cells = list(
            self.sheet.get_selected_cells()
        )  # ✅ 'set'을 리스트로 변환
        if not selected_cells:
            return

        row, col = selected_cells[0]
        print(f"[int matrix] self.material_rows : {self.material_rows}")

        SWM_names = [
            "Floor",
            "Skirt",
            "Wall",
            "Ceiling",
        ]

        SWM_idxes = [self.material_rows.index(x) for x in SWM_names]
        print(f"SWM_idxes {SWM_idxes}")

        row_dist = [x - row for x in SWM_idxes]
        min_row_dist = go(
            row_dist,
            filter(lambda x: x < 0),
            max,
        )
        print(f"row_dist {row_dist}")
        print(f"min_row_dist {min_row_dist}")
        parent_SWM_idx = row_dist.index(min_row_dist)
        print(f"parent_SWM_idx {parent_SWM_idx}")

        SWM_name = SWM_names[parent_SWM_idx]
        material_name = self.material_rows[row]  # ✅ 원래 데이터 가져오기
        material_full_name = " | ".join([SWM_name, material_name])
        room = self.filtered_rooms[col]
        roomName_asDBformat = room.replace("_", "\t")

        # ✅ 대분류(바닥, 천장, 걸레받이, 벽)는 체크 불가능
        if row in self.category_rows:
            return

        # ✅ 현재 상태 반전 (체크/해제)
        # self.check_status[room][material_name] = not self.check_status[room][
        #     material_name
        # ]
        tgt_room_db = go(
            state.team_std_info[self.data_kind]["children"],
            filter(lambda x: x["name"] == roomName_asDBformat),
            next,
            lambda x: x["children"],
        )

        tgt_room_material_names = go(
            tgt_room_db,
            map(lambda x: x[2]),
            list,
        )

        print(f"[int matrix] tgt_room_material_names : {tgt_room_material_names}")
        print(f"[int matrix] material_name : {material_name}")

        def delete_assign_forRoom(roomName, material_full_name):
            # print(f"[delete_assign_forRoom] roomName {roomName}")
            # print(f"[delete_assign_forRoom] deleting start")
            data = state.team_std_info[self.data_kind]["children"]

            for i in data:
                if (
                    i["name"] == roomName
                    and i["values"][1] == state.current_building.get()
                ):
                    for idx, c in enumerate(i["children"]):
                        # print(f"[delete_assign_forRoom] deleting stt {c}")
                        if c[2] == material_full_name:
                            res = i["children"].pop(idx)
                            # print(f"[delete_assign_forRoom] deleting end {res}")

        def add_assign_forRoom(roomName, material_full_name):
            pjt_SWM_key = " | ".join(["00 Room Finish", material_full_name])
            print(f"[add_assign_forRoom] pjt_SWM_key {pjt_SWM_key}")
            wmStr = state.team_std_info["project-SWM"][pjt_SWM_key]

            print(f"[add_assign_forRoom] wmStr {wmStr}")

        # DB 상태에 따라 체크하는 코드를 update로 옮기고,-> 완료
        # 여기서는 더블 클릭에 따라 DB를 조작하도록
        if material_full_name in tgt_room_material_names:
            # self.sheet.set_cell_data(row, col, "✅")
            # DB에서 해당 항목 삭제
            delete_assign_forRoom(roomName_asDBformat, material_full_name)

        else:
            # self.sheet.set_cell_data(row, col, "")
            # DB에 해당 항목 추가
            add_assign_forRoom(roomName_asDBformat, material_full_name)

        # # ✅ 체크된 상태에 따라 셀 내용 업데이트
        # self.sheet.set_cell_data(
        #     row, col, "✅" if self.check_status[room][material_name] else ""
        # )

        # # ✅ 마감 사양 데이터 업데이트
        # self.update_finish_data(room)

        state.observer_manager.notify_observers(state)
