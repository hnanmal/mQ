import tkinter as tk
from tkinter import simpledialog


class PasteLocationDialog(simpledialog.Dialog):
    def body(self, master):
        self.var = tk.StringVar(value="name")

        tk.Label(master, text="Where do you want to paste the text?").pack(pady=10)

        self.name_radio = tk.Radiobutton(
            master, text="Name", variable=self.var, value="name"
        )
        self.name_radio.pack(anchor="w")

        self.description_radio = tk.Radiobutton(
            master, text="Description", variable=self.var, value="description"
        )
        self.description_radio.pack(anchor="w")

        return self.name_radio  # Initial focus

    def apply(self):
        self.result = self.var.get()


def ask_paste_location():
    """Prompt user to select whether to paste into Name or Description."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    dialog = PasteLocationDialog(root, "Paste Location")
    return dialog.result


def confirm_level_change():
    """Prompt the user to confirm the level change."""
    from tkinter import messagebox

    return messagebox.askokcancel(
        "확인", "선택한 항목의 레벨이 변경됩니다. 이동하시겠습니까?"
    )
