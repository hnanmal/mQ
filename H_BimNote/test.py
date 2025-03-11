import tkinter as tk
from tkinter import ttk


class TreeviewHighlighter:
    def __init__(self, root):
        self.tree = ttk.Treeview(root, columns=("Values",), show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("Values", text="Values")

        # 트리뷰에 데이터 삽입 (부모-자식 관계)
        self.populate_tree()

        # 스타일 및 태그 설정
        self.style = ttk.Style()
        self.style.configure(
            "Treeview.Highlighted.TLabel", foreground="red"
        )  # 스타일 정의

        # 버튼 추가 (강조 기능 실행)
        highlight_button = tk.Button(
            root, text="Highlight Matches", command=self.highlight_matching_items
        )
        highlight_button.pack(pady=5)

        self.tree.pack(expand=True, fill="both")

    def populate_tree(self):
        """트리뷰에 부모-자식 관계로 데이터 추가"""
        parent1 = self.tree.insert(
            "", "end", text="Parent 1", values=("Hello, world!",)
        )
        self.tree.insert(
            parent1,
            "end",
            text="Child 1.1",
            values=("Matching Value",),
            tags=("highlight",),
        )
        self.tree.insert(parent1, "end", text="Child 1.2", values=("No match",))

        parent2 = self.tree.insert(
            "", "end", text="Parent 2", values=("Contains: Match!",)
        )
        self.tree.insert(parent2, "end", text="Child 2.1", values=("Some other text",))
        self.tree.insert(parent2, "end", text="Child 2.2", values=("Match found",))

        # 태그 스타일 적용
        self.tree.tag_configure("highlight", foreground="red")

    def highlight_matching_items(self):
        """values에 특정 문자열이 포함된 항목을 붉은색으로 표시"""
        search_term = "Match"  # 찾을 문자열

        for item in self.tree.get_children():
            self.check_and_highlight(item, search_term)

    def check_and_highlight(self, item, search_term):
        """재귀적으로 트리 아이템을 검사하고, 특정 문자열이 포함된 경우 색상을 변경"""
        values = self.tree.item(item, "values")

        if any(
            search_term in str(value) for value in values
        ):  # 값에 특정 문자열 포함 여부 검사
            self.tree.item(item, tags=("highlight",))  # 태그 적용

        for child in self.tree.get_children(item):  # 재귀적으로 자식 항목 검사
            self.check_and_highlight(child, search_term)


# 실행
root = tk.Tk()
root.title("Treeview Highlighter Example")
root.geometry("400x300")

app = TreeviewHighlighter(root)

root.mainloop()
