import tkinter as tk


def toggle_stdGWM_widget_mode(state, sheet, edit_mode_var):  ##sheet를 탭으로 바꿔서?
    """시트의 편집 가능 여부를 전환하는 함수"""
    mode = edit_mode_var.get()
    if mode == "edit":
        sheet.enable_bindings()  # 모든 기본 바인딩 활성화
        state.std_matching_add_btn.config(state=tk.NORMAL)
        state.std_matching_del_btn.config(state=tk.NORMAL)
        state.std_matching_listbox.config(bg="white", fg="black")

        state.log_widget.write("Sheet is now in Edit Mode")
    elif mode == "locked":
        # 편집 관련 바인딩을 비활성화하여 편집을 잠금
        sheet.disable_bindings(
            "edit_cell",
            "delete",
            "insert_row",
            "delete_row",
            "paste",
        )

        state.std_matching_add_btn.config(state=tk.DISABLED)
        state.std_matching_del_btn.config(state=tk.DISABLED)
        state.std_matching_listbox.config(bg="lightgray", fg="black")

        state.log_widget.write("Sheet is now in Locked Mode")
