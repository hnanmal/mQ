import tkinter as tk
from tkinter import ttk


class TreeviewSearch:
    def __init__(self, root):
        self.tree = ttk.Treeview(root, columns=("Values",), show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("Values", text="Values")

        # 샘플 데이터 추가
        self.populate_tree()

        # 검색 입력 필드 및 버튼
        search_frame = tk.Frame(root)
        search_frame.pack(pady=5)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        search_button = tk.Button(
            search_frame, text="Search", command=self.search_items
        )
        search_button.pack(side="left")

        next_button = tk.Button(search_frame, text="Next", command=self.next_match)
        next_button.pack(side="left")

        self.tree.pack(expand=True, fill="both")

        # 검색 결과 저장용 변수
        self.matched_items = []  # 검색어가 포함된 항목 ID 리스트
        self.current_index = -1  # 현재 선택된 검색 결과의 인덱스

    def populate_tree(self):
        """트리뷰에 샘플 데이터 삽입"""
        parent1 = self.tree.insert("", "end", text="Apple", values=("Fruit",))
        self.tree.insert(parent1, "end", text="Apple Pie", values=("Dessert",))
        self.tree.insert(parent1, "end", text="Apple Juice", values=("Drink",))

        parent2 = self.tree.insert("", "end", text="Banana", values=("Fruit",))
        self.tree.insert(parent2, "end", text="Banana Bread", values=("Dessert",))
        self.tree.insert(parent2, "end", text="Banana Smoothie", values=("Drink",))

        parent3 = self.tree.insert("", "end", text="Cherry", values=("Fruit",))
        self.tree.insert(parent3, "end", text="Cherry Tart", values=("Dessert",))
        self.tree.insert(parent3, "end", text="Cherry Soda", values=("Drink",))

    def search_items(self):
        """검색어가 포함된 항목 찾기"""
        search_text = self.search_entry.get().lower()
        self.matched_items = []  # 기존 검색 결과 초기화
        self.current_index = -1

        if not search_text:
            return  # 검색어가 없으면 종료

        # 모든 트리 항목을 검색
        for item in self.tree.get_children():
            self.find_matching_items(item, search_text)

        # 검색 결과가 있으면 첫 번째 항목으로 이동
        if self.matched_items:
            self.current_index = 0
            self.highlight_and_focus(self.matched_items[self.current_index])

    def find_matching_items(self, item, search_text):
        """재귀적으로 트리 아이템을 검사하고, 검색어가 포함된 경우 리스트에 추가"""
        item_text = self.tree.item(item, "text").lower()
        item_values = [str(val).lower() for val in self.tree.item(item, "values")]

        # 검색어가 포함된 경우 저장
        if search_text in item_text or any(search_text in val for val in item_values):
            self.matched_items.append(item)

        # 자식 항목도 검사
        for child in self.tree.get_children(item):
            self.find_matching_items(child, search_text)

    def next_match(self):
        """검색 결과를 순차적으로 이동"""
        if not self.matched_items:
            return  # 검색 결과가 없으면 종료

        self.current_index += 1
        if self.current_index >= len(self.matched_items):
            self.current_index = 0  # 마지막까지 가면 처음으로 돌아감

        self.highlight_and_focus(self.matched_items[self.current_index])

    def highlight_and_focus(self, item):
        """선택된 항목을 강조하고 포커스 이동"""
        self.tree.selection_set(item)  # 항목 선택
        self.tree.focus(item)  # 포커스 이동
        self.tree.see(item)  # 트리뷰가 자동으로 스크롤하여 보이게 함


# 실행
root = tk.Tk()
root.title("Treeview Search Example")
root.geometry("400x300")

app = TreeviewSearch(root)

root.mainloop()
