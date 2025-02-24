# src/core/file_utils.py

import json
from tkinter import filedialog, ttk

import openpyxl

from src.core.fp_utils import *
from src.core.app_update import APP_VERSION
from src.views.widget.widget import (
    open_dialog,
    open_filesave_dialog,
    open_filesave_dialog_opening,
)


def save_to_json_teamStdInfo(state, _file_path=None):
    # 파일 저장 위치 선택
    if _file_path and _file_path != "resource/PlantArch_BIM Standard.bnote":
        file_path = _file_path
    else:
        file_path = filedialog.asksaveasfilename(
            defaultextension=state.defaultextension, filetypes=state.filetypes
        )
        if file_path:
            state.current_filepath = file_path
        else:
            return  # 파일 경로가 없으면 저장 취소

    # 상태 객체에서 데이터를 저장
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(state.team_std_info, file, indent=4, ensure_ascii=False)
            # json.dump(state.project_info, file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {file_path}")
        state.root.title(
            f"B-note  {APP_VERSION} :: Hyundai Engineering Plant Architecture Bim Note"
            + "    " * 22
            + f"[   {state.current_filepath}   ]"
        )
        open_dialog(
            state,
            f"데이터가 \n\n ◾ {state.current_filepath} \n\n에 저장 되었습니다.",
            width=800,
        )

        exist_recent_files = go(
            state.recent_files["recent_items"],
            map(lambda x: x["name"]),
            list,
        )
        if file_path != "resource/PlantArch_BIM Standard.bnote":
            if file_path not in exist_recent_files:
                state.recent_files["recent_items"].insert(0, {"name": file_path})
            elif file_path in exist_recent_files:
                tgt_idx = exist_recent_files.index(file_path)
                tgt = state.recent_files["recent_items"].pop(tgt_idx)
                state.recent_files["recent_items"].insert(0, tgt)
            with open("resource/recent_files.json", "w", encoding="utf-8") as file:
                json.dump(state.recent_files, file, indent=4, ensure_ascii=False)

        state.recent_page.load_items()

        state.init_db_hash = state.get_db_hash()

    except Exception as e:
        print(f"Error saving data to JSON: {e}")


def load_from_json(state, _file_path=None):
    # 파일 열기 위치 선택
    if _file_path:
        file_path = _file_path

        state.current_filepath = file_path
    else:
        file_path = filedialog.askopenfilename(filetypes=state.filetypes)
        if file_path:
            state.current_filepath = file_path
        else:
            state.log_widget.write("파일 로드 취소\n")
            return  # 파일 경로가 없으면 로드 취소

    # JSON 파일에서 데이터 로드
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            loaded_data = json.load(file)

            state.update_team_standard_info(loaded_data, data_kind="std-GWM")
            state.update_team_standard_info(loaded_data, data_kind="std-SWM")
            state.update_team_standard_info(loaded_data, data_kind="common-input")
            state.update_team_standard_info(loaded_data, data_kind="std-familylist")
            state.update_team_standard_info(loaded_data, data_kind="std-calcdict")
            state.update_team_standard_info(loaded_data, data_kind="project-info")
            state.update_team_standard_info(loaded_data, data_kind="project-GWM")
            state.update_team_standard_info(loaded_data, data_kind="project-SWM")
            state.update_team_standard_info(
                loaded_data, data_kind="project-buildinglist"
            )
            state.update_team_standard_info(loaded_data, data_kind="project-assigntype")
            state.update_team_standard_info(
                loaded_data, data_kind="project-assigntype-WM"
            )
            state.update_team_standard_info(loaded_data, data_kind="dynamo-calculation")

            if loaded_data.get("WMs"):
                state.update_team_standard_info(loaded_data, data_kind="WMs")
            else:
                loadedWMs = load_from_excel(
                    state, _file_path="resource/WorkMaster_DB.xlsx"
                )[6:]
                state.update_team_standard_info({"WMs": loadedWMs}, data_kind="WMs")

        state.log_widget.write(f"Data successfully loaded from {file_path}\n")
        state.root.title(
            f"B-note  {APP_VERSION} :: Hyundai Engineering Plant Architecture Bim Note"
            + "    " * 22
            + f"[   {state.current_filepath}   ]"
        )
        open_dialog(
            state,
            f"데이터가 \n\n ◾ {state.current_filepath} \n\n으로부터 로드 되었습니다.",
            width=800,
        )

        exist_recent_files = go(
            state.recent_files["recent_items"],
            map(lambda x: x["name"]),
            list,
        )
        if file_path != "resource/PlantArch_BIM Standard.bnote":
            if file_path not in exist_recent_files:
                state.recent_files["recent_items"].insert(0, {"name": file_path})
            elif file_path in exist_recent_files:
                tgt_idx = exist_recent_files.index(file_path)
                tgt = state.recent_files["recent_items"].pop(tgt_idx)
                state.recent_files["recent_items"].insert(0, tgt)
            with open("resource/recent_files.json", "w", encoding="utf-8") as file:
                json.dump(state.recent_files, file, indent=4, ensure_ascii=False)

        state.recent_page.load_items()

        state.init_db_hash = state.get_db_hash()

        return True
    except Exception as e:
        state.log_widget.write(f"Error loading data from JSON: {e}\n")
        return False


def on_closing(root, state):
    """앱 종료 시 저장 확인창을 띄우고, 선택에 따라 동작을 수행."""
    if state.init_db_hash != "not loaded yet":
        is_change = state.init_db_hash != state.get_db_hash()

        if is_change:
            open_filesave_dialog(
                state,
                "변경 내용을 이 파일에 저장하시겠습니까?",
            )
        else:
            root.destroy()
    else:
        root.destroy()


def on_opening(state):
    """앱 종료 시 저장 확인창을 띄우고, 선택에 따라 동작을 수행."""
    if state.init_db_hash != "not loaded yet":
        is_change = state.init_db_hash != state.get_db_hash()

        if is_change:
            open_filesave_dialog_opening(
                state,
                "변경 내용을 이 파일에 저장하시겠습니까?",
            )
        else:
            load_from_json(state)
    else:
        load_from_json(state)


def load_from_excel(state, _file_path=None):
    # 파일 열기 위치 선택
    if _file_path:
        file_path = _file_path
    else:
        file_path = filedialog.askopenfilename(filetypes=state.filetypes)
        if not file_path:
            return  # 파일 경로가 없으면 로드 취소

    try:
        # Excel 파일에서 데이터 로드
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # 시트 데이터를 리스트 형태로 저장
        sheet_data = []
        for row in sheet.iter_rows(values_only=True):
            sheet_data.append(list(row))

        # # tksheet에 데이터 설정
        # state.update_team_standard_info(sheet_data[6:], data_kind="WMs")
        # print(f"Data successfully loaded from {file_path}")
        return sheet_data
    except Exception as e:
        print(f"Error loading data from Excel: {e}")


# Load HTML file content
def load_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()
