from tksheet import Sheet
import tkinter as tk


class WordWrapSheetApp:
    def __init__(self, root):
        self.root = root
        self.sheet = Sheet(
            root,
            data=[["Short text", "This is a long piece of text that needs wrapping."]],
            height=200,
            width=400,
        )
        self.sheet.pack(expand=True, fill="both")

        # Bind column width change to trigger wrapping
        self.sheet.extra_bindings([("column_width_resize_end", self.on_column_resize)])

        # Initial wrapping
        self.apply_wrap()

    def wrap_text(self, text, width):
        """
        Wrap text to fit within a given width.
        """
        if not text or not isinstance(text, str):
            return text
        max_chars_per_line = max(1, width // 7)  # Approximate character width in pixels
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > max_chars_per_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = f"{current_line} {word}".strip()

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    def apply_wrap(self):
        """
        Apply wrapping to all cells based on their column widths.
        """
        wrapped_data = []
        for row_index, row in enumerate(self.sheet.get_sheet_data()):
            wrapped_row = []
            for col_index, cell in enumerate(row):
                width = self.sheet.column_width(col_index)
                wrapped_row.append(self.wrap_text(cell, width))
            wrapped_data.append(wrapped_row)

        self.sheet.set_sheet_data(wrapped_data)

    def on_column_resize(self, event):
        """
        Re-wrap text when columns are resized.
        """
        self.apply_wrap()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Word Wrap in tksheet")
    app = WordWrapSheetApp(root)
    root.mainloop()
