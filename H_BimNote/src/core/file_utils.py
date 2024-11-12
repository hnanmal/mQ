import json
from tkinter import filedialog, ttk


def save_to_json_teamStdInfo(state):
    # 파일 저장 위치 선택
    file_path = filedialog.asksaveasfilename(
        defaultextension=state.defaultextension, filetypes=state.filetypes
    )
    if not file_path:
        return  # 파일 경로가 없으면 저장 취소

    # 상태 객체에서 데이터를 저장
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(state.team_std_info, file, indent=4, ensure_ascii=False)
            # json.dump(state.project_info, file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")


def load_from_json(state, _file_path=None):
    # 파일 열기 위치 선택
    if _file_path:
        file_path = _file_path
    else:
        file_path = filedialog.askopenfilename(filetypes=state.filetypes)
        if not file_path:
            return  # 파일 경로가 없으면 로드 취소

    # JSON 파일에서 데이터 로드
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            loaded_data = json.load(file)

            state.update_team_standard_info(loaded_data)

            # state.update_project_info(loaded_data.get("project_info", {}))
            # state.family_standard_data = loaded_data.get("family_standard_data", {})
        print(f"Data successfully loaded from {file_path}")
    except Exception as e:
        print(f"Error loading data from JSON: {e}")
