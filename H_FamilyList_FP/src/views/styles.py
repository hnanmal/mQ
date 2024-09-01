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

    font_level_1 = font.Font(family="Helvetica", size=16, weight="bold")
    font_level_4 = font.Font(family="Helvetica", size=12)
    default_font = font.Font(family="Helvetica", size=9)

    tree.tag_configure("Level1", font=font_level_1, background="lightgreen")
    tree.tag_configure("Level4", font=font_level_4, foreground="blue")
    tree.tag_configure("OtherLevels", font=default_font)
