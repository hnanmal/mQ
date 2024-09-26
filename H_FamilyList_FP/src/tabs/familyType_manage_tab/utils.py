# src/tabs/familyType_manage_tab/utils.py
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from src.tabs.input_common_tab.utils import create_defaultTreeview


def creat_combo_buildingList(state, frame, data):
    # project_info = json.dump(state.project_info_.get())
    # combo_list = list(
    #     map(lambda x: x["building_name"], state.project_info["building_list"])
    # )
    combo_list = data
    # print(state.project_info_.get())
    # print(state.project_info)
    comboBox = ttk.Combobox(frame)
    comboBox.config(height=5)  # 높이 설정
    comboBox.config(textvariable=combo_list)  # 나타낼 항목 리스트(a) 설정
    comboBox.config(state="readonly")  # 콤보 박스에 사용자가 직접 입력 불가
    comboBox.set("대상 빌딩 선택")  # 맨 처음 나타낼 값 설정
    comboBox.pack(side=tk.TOP, padx=10, pady=10, anchor="w")


def save_project_roomType_info(state):
    project_info_ = state.project_info

    file_path = filedialog.asksaveasfilename(
        defaultextension=".hpjt",  # Default file extension
        filetypes=[("HPJT files", "*.hpjt"), ("All files", "*.*")],
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(project_info_, f, ensure_ascii=False, indent=4)
    state.logging_text_widget.write(f"Project Info saved to {file_path}\n")
