# src/views/styles.py
from tkinter import font, ttk


def configure_styles(tree):
    style = ttk.Style()
    style.configure("Treeview", rowheight=35)
    style.map(
        "Treeview",
        background=[("selected", "blue")],
        foreground=[("selected", "white")],
    )

    comm_font = "Malgun Gothic"
    font_level_0 = font.Font(family=comm_font, size=14, weight="bold")
    font_level_4 = font.Font(family=comm_font, size=12, weight="bold")
    default_font = font.Font(family=comm_font, size=10)

    tree.tag_configure("Level0", font=font_level_0, background="#D6EFD8")
    tree.tag_configure("Level4", font=font_level_4, foreground="blue")
    tree.tag_configure("OtherLevels", font=default_font)
