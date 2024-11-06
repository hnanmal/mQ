import json
from tkinter import filedialog, ttk


def save_to_json(state):
    # 파일 저장 위치 선택
    file_path = filedialog.asksaveasfilename(
        defaultextension=state.defaultextension, filetypes=state.filetypes
    )
    if not file_path:
        return  # 파일 경로가 없으면 저장 취소

    # 상태 객체에서 데이터를 저장
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(state.project_info, file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")
