# src/controllers/clipboard_management.py

import tkinter as tk

from src.utils.tree_utils import (
    copy_treeview_items,
    extract_treeview_data,
    paste_treeview_items,
)


def copy_to_clipboard(tree, selected_items, state):

    clipboard_data = []  # 리스트로 초기화
    for item_id in selected_items:
        try:
            item_data = extract_treeview_data(tree, item_id)  # 개별 아이템 처리
            # item_data = tree.item(item_id)  # 개별 아이템 처리
            print(f"Extracted item data: {item_data}")
            clipboard_data.append(item_data)
        except Exception as e:
            print(f"Error extracting data for item_id {item_id}: {e}")

    # 상태 객체에 클립보드 데이터를 저장
    state.set_clipboard_data(clipboard_data)

    if clipboard_data:
        print(f"Copied clipboard_data: {clipboard_data}, type: {type(clipboard_data)}")
    else:
        print("No valid items to copy.")


def paste_from_clipboard(tree, target_item, clipboard_data):
    # state.set_clipboard_data(clipboard_data)
    """클립보드에서 데이터를 붙여넣음."""
    if clipboard_data:
        paste_treeview_items(tree, target_item, clipboard_data)
        print(f"Pasted items: {clipboard_data}")  # 디버깅 출력


def paste_external_data(tree, target_items, paste_to):
    clipboard_text = tk.Tk().clipboard_get()
    clipboard_lines = clipboard_text.splitlines()

    for i, item in enumerate(target_items):
        if i >= len(clipboard_lines):
            break
        current_values = list(tree.item(item, "values"))
        if paste_to == "name":
            current_values[0] = clipboard_lines[i]
        elif paste_to == "description":
            current_values[1] = clipboard_lines[i]
        tree.item(item, values=tuple(current_values))
