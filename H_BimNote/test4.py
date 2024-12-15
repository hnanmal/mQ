import tkinter as tk
from tksheet import Sheet


def toggle_checkbox(event):
    """더블 클릭으로 체크박스 상태 토글"""
    selected = sheet.get_currently_selected()
    if selected:
        row, col = selected
        if col == 0:  # 체크박스가 있는 첫 번째 열
            current_value = sheet.get_cell_data(row, col)
            sheet.set_cell_data(row, col, not current_value)  # 상태 반전


def get_checked_items():
    """체크된 항목 출력"""
    checked_items = []
    for iid in sheet.get_children():
        item_data = sheet.item(iid)
        if item_data["values"][0]:  # 첫 번째 열의 값이 True인 항목
            checked_items.append(item_data["text"])
    print("Checked Items:", checked_items)


# Tkinter 윈도우 생성
root = tk.Tk()
root.title("tksheet Treeview with Checkboxes Example")

# tksheet 위젯 생성 (treeview 모드 활성화)
sheet = Sheet(root, treeview=True, headers=["Select", "Name"], height=400, width=600)
sheet.pack(expand=True, fill="both")

# 트리뷰 데이터
tree_data = [
    ["id1", "", False, "Category 1"],  # 최상위 노드
    ["id2", "id1", False, "Subcategory 1.1"],  # id1의 하위 노드
    ["id3", "id1", True, "Subcategory 1.2"],
    ["id4", "id3", False, "Item 1.2.1"],  # id3의 하위 노드
    ["id5", "", False, "Category 2"],  # 새로운 최상위 노드
    ["id6", "id5", True, "Subcategory 2.1"],
    ["id7", "id6", False, "Item 2.1.1"],
]

# 트리뷰 데이터 빌드
sheet.tree_build(
    data=[[row[0], row[1], row[2], row[3]] for row in tree_data],
    iid_column=0,  # ID 열
    parent_column=1,  # 부모 ID 열
    text_column=3,  # 트리뷰에 표시할 텍스트 열
    include_iid_column=False,  # ID 열을 데이터에 표시하지 않음
    include_parent_column=False,  # 부모 ID 열을 데이터에 표시하지 않음
)

# 첫 번째 열에 Boolean 값 설정
for idx, row in enumerate(tree_data):
    sheet.set_cell_data(idx, 0, row[2])

# 체크박스 상태를 더블 클릭으로 토글
sheet.bind("<Double-1>", toggle_checkbox)

# 버튼 생성
btn_get_checked = tk.Button(root, text="Get Checked Items", command=get_checked_items)
btn_get_checked.pack(pady=10)

# Tkinter 메인 루프 시작
root.mainloop()
