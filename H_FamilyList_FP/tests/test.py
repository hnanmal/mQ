import tkinter as tk
from tkinter import ttk, filedialog, Text
import json


class MemoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memo Pad App")
        self.state = {"project_info": {}, "current_label": ""}

        # Create UI
        self.create_ui()

    def create_ui(self):
        # Label selection list
        self.label_listbox = tk.Listbox(self.root)
        self.label_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.label_listbox.bind("<<ListboxSelect>>", self.on_label_select)

        # Memo pad (Text widget for writing notes)
        self.memo_pad = Text(self.root, height=10, width=40)
        self.memo_pad.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Buttons to save and load project info
        load_button = tk.Button(
            self.root, text="Load Project Info", command=self.load_project_info
        )
        load_button.pack(side=tk.TOP)

        save_button = tk.Button(self.root, text="Save Note", command=self.save_note)
        save_button.pack(side=tk.TOP)

    def on_label_select(self, event):
        """Handle label selection and display the associated memo."""
        # Get the selected label
        selection = self.label_listbox.curselection()
        if selection:
            selected_label = self.label_listbox.get(selection[0])
            self.state["current_label"] = selected_label

            # Clear memo pad and load associated note from the state
            self.memo_pad.delete("1.0", tk.END)
            note = (
                self.state["project_info"]["building_list"]
                .get(selected_label, {})
                .get("note", "")
            )
            self.memo_pad.insert(tk.END, note)

    def save_note(self):
        """Save the note for the selected label."""
        selected_label = self.state["current_label"]
        note = self.memo_pad.get("1.0", tk.END).strip()

        # Update the note in the state
        if selected_label in self.state["project_info"]["building_list"]:
            self.state["project_info"]["building_list"][selected_label]["note"] = note
            print(f"Note saved for {selected_label}: {note}")

    def load_project_info(self):
        """Load project info and populate label list and memos."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)

            # Save loaded data to state
            self.state["project_info"] = loaded_data

            # Populate label listbox
            self.label_listbox.delete(0, tk.END)
            for building in loaded_data["building_list"]:
                self.label_listbox.insert(tk.END, building)

            print(f"Project Info loaded from {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoApp(root)
    root.mainloop()
