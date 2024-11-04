import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk, Scale, Scrollbar
import ast
import sqlite3
import yaml
import os


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.classes = {}
        self.functions = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append(f"{node.module if node.module else ''}.{alias.name}")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_info = {
            "methods": [],
            "properties": [],
            "bases": [self.get_base_name(b) for b in node.bases],
            "docstring": ast.get_docstring(node),
        }
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = {
                    "name": item.name,
                    "args": [a.arg for a in item.args.args],
                    "returns": self.get_returns(item),
                    "docstring": ast.get_docstring(item),
                }
                class_info["methods"].append(method_info)
                if item.name == "__init__":
                    for stmt in item.body:
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if (
                                    isinstance(target, ast.Attribute)
                                    and isinstance(target.value, ast.Name)
                                    and target.value.id == "self"
                                ):
                                    class_info["properties"].append(target.attr)
        self.classes[node.name] = class_info
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Capture properties defined at the class level
        if isinstance(node.parent, ast.ClassDef):
            class_name = node.parent.name
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.classes[class_name]["properties"].append(target.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Determine if the function is a method or a standalone function
        if isinstance(node.parent, ast.ClassDef):
            # It's a method inside a class
            class_name = node.parent.name
            method_info = {
                "name": node.name,
                "args": [a.arg for a in node.args.args],
                "returns": self.get_returns(node),
                "docstring": ast.get_docstring(node),
            }
            self.classes[class_name]["methods"].append(method_info)
        elif not isinstance(
            node.parent, (ast.FunctionDef, ast.AsyncFunctionDef)
        ):  # Ignore functions defined inside methods or functions
            # It's a standalone function
            function_info = {
                "name": node.name,
                "args": [a.arg for a in node.args.args],
                "returns": self.get_returns(node),
                "docstring": ast.get_docstring(node),
            }
            self.functions.append(function_info)
        self.generic_visit(node)

    def get_base_name(self, base):
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id}.{base.attr}"
        return "Unknown"

    def get_returns(self, node):
        if isinstance(node.returns, ast.Name):
            return node.returns.id
        elif isinstance(node.returns, ast.Attribute):
            return f"{node.returns.value.id}.{node.returns.attr}"
        return None

    def parse_code(self, code):
        self.imports.clear()
        self.classes.clear()
        self.functions.clear()
        tree = ast.parse(code)
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        self.visit(tree)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Code Parser with DB Save")
        self.geometry("1400x900")

        self.analyzer = CodeAnalyzer()
        self.create_widgets()
        self.create_database()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5)
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        parse_button = tk.Button(button_frame, text="Parse", command=self.parse_code)
        parse_button.pack(side=tk.LEFT, padx=5)

        select_folder_button = tk.Button(
            button_frame,
            text="Select Project Folder",
            command=self.select_project_folder,
        )
        select_folder_button.pack(side=tk.LEFT, padx=5)

        # Treeview to display the parsed code structure
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.heading("#0", text="Code Structure", anchor="w")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add vertical scrollbar to the treeview
        tree_scrollbar_y = Scrollbar(
            self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        tree_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scrollbar_y.set)

        # Add horizontal scrollbar to the treeview
        tree_scrollbar_x = Scrollbar(
            self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        tree_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=tree_scrollbar_x.set)

        # Scale to control the level of expansion of the treeview
        self.level_scale = Scale(
            self,
            from_=1,
            to=10,
            orient="horizontal",
            label="Expand Level",
            command=self.expand_tree,
        )
        self.level_scale.pack(pady=5)
        self.level_scale.bind("<MouseWheel>", self.on_mouse_wheel)

    def create_database(self):
        # Create a SQLite database to store parsed code details
        self.conn = sqlite3.connect("code_analysis.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS code_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imports TEXT,
                classes TEXT,
                functions TEXT
            )
        """
        )
        self.conn.commit()

    def parse_code(self):
        code = self.text_area.get("1.0", tk.END)
        self.analyzer.parse_code(code)
        self.display_tree()

    def display_tree(self):
        # Clear existing tree items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add imports to the treeview
        imports_id = self.tree.insert("", "end", text="Imports", tags=("key",))
        for imp in self.analyzer.imports:
            self.tree.insert(imports_id, "end", text=imp)

        # Add classes, properties, and methods to the treeview
        for cls, details in self.analyzer.classes.items():
            class_id = self.tree.insert("", "end", text=f"Class: {cls}", tags=("key",))
            self.tree.insert(
                class_id, "end", text=f"Bases: {', '.join(details['bases'])}"
            )
            if details.get("docstring"):
                self.tree.insert(
                    class_id, "end", text=f"Docstring: {details['docstring']}"
                )

            properties_id = self.tree.insert(
                class_id, "end", text="Properties", tags=("key",)
            )
            for prop in details["properties"]:
                self.tree.insert(properties_id, "end", text=prop, tags=("property",))

            methods_id = self.tree.insert(
                class_id, "end", text="Methods", tags=("key",)
            )
            for method in details["methods"]:
                method_id = self.tree.insert(
                    methods_id,
                    "end",
                    text=f"Method: {method['name']}",
                    tags=("method", "bold"),
                )
                self.tree.insert(
                    method_id, "end", text=f"Args: {', '.join(method['args'])}"
                )
                if method["returns"]:
                    self.tree.insert(
                        method_id, "end", text=f"Returns: {method['returns']}"
                    )
                if method.get("docstring"):
                    self.tree.insert(
                        method_id, "end", text=f"Docstring: {method['docstring']}"
                    )

        # Add standalone functions to the treeview
        functions_id = self.tree.insert("", "end", text="Functions", tags=("key",))
        for func in self.analyzer.functions:
            func_id = self.tree.insert(
                functions_id,
                "end",
                text=f"Function: {func['name']}",
                tags=("method", "bold"),
            )
            self.tree.insert(
                func_id,
                "end",
                text=f"Args: {', '.join(func['args'])}",
                tags=("method",),
            )
            if func["returns"]:
                self.tree.insert(
                    func_id, "end", text=f"Returns: {func['returns']}", tags=("method",)
                )
            if func.get("docstring"):
                self.tree.insert(
                    func_id,
                    "end",
                    text=f"Docstring: {func['docstring']}",
                    tags=("method",),
                )

        # Apply the style to key rows, properties, and methods
        self.tree.tag_configure("key", font=("TkDefaultFont", 10, "bold"))
        self.tree.tag_configure("property", foreground="blue")
        self.tree.tag_configure("method", foreground="purple")
        self.tree.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))

    def expand_tree(self, level):
        # Expand or collapse the tree up to the specified level
        level = int(level)
        for item in self.tree.get_children():
            self._expand_or_collapse_tree(item, current_level=1, target_level=level)

    def _expand_or_collapse_tree(self, item, current_level, target_level):
        if current_level <= target_level:
            self.tree.item(item, open=True)
        else:
            self.tree.item(item, open=False)
        for child in self.tree.get_children(item):
            self._expand_or_collapse_tree(child, current_level + 1, target_level)

    def on_mouse_wheel(self, event):
        # Adjust the level scale with the mouse wheel
        current_value = self.level_scale.get()
        delta = 1 if event.delta > 0 else -1
        new_value = max(1, min(10, current_value + delta))
        self.level_scale.set(new_value)
        self.expand_tree(new_value)

    def save_to_yaml(self):
        data = {
            "imports": self.analyzer.imports,
            "classes": self.analyzer.classes,
            "functions": self.analyzer.functions,
        }
        file_path = filedialog.asksaveasfilename(
            defaultextension=".yaml", filetypes=[("YAML files", "*.yaml")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
                messagebox.showinfo(
                    "Success", "Parsed data saved to YAML successfully!"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_from_yaml(self):
        file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)
                    self.analyzer.imports = data.get("imports", [])
                    self.analyzer.classes = data.get("classes", {})
                    self.analyzer.functions = data.get("functions", [])
                    self.display_tree()
                messagebox.showinfo("Success", "YAML data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def select_project_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.project_folder_path = folder_path
            self.project_structure = {}
            self.get_project_structure(folder_path)
            self.display_project_tree()

    def get_project_structure(self, folder_path, structure=None):
        if structure is None:
            structure = self.project_structure

        for root, dirs, files in os.walk(folder_path):
            relative_path = os.path.relpath(root, folder_path)
            if relative_path == ".":
                relative_path = ""

            # Add folders
            folders = relative_path.split(os.sep)
            current_dict = structure
            for folder in folders:
                if folder not in current_dict:
                    current_dict[folder] = {}
                current_dict = current_dict[folder]

            # Add files
            current_dict["files"] = [f for f in files if f.endswith(".py")]

    def display_project_tree(self):
        # Clear existing tree items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add top-level project item with 'pjt' prefix
        project_name = os.path.basename(self.project_folder_path)
        if not project_name:
            project_name = "Unnamed Project"
        project_id = self.tree.insert(
            "", "end", text=f"pjt: {project_name}", tags=("key",)
        )

        def add_items(parent, structure, folder_path):
            for key, value in structure.items():
                if key == "files":
                    for file in value:
                        file_path = os.path.join(folder_path, file)
                        file_id = self.tree.insert(
                            parent, "end", text=file, tags=("key",)
                        )
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                code = f.read()
                        except UnicodeDecodeError:
                            with open(file_path, "r", encoding="latin-1") as f:
                                code = f.read()

                        self.analyzer.parse_code(code)
                        self.add_parsed_file_to_tree(file_id)
                else:
                    folder_id = self.tree.insert(parent, "end", text=key, tags=("key",))
                    add_items(folder_id, value, os.path.join(folder_path, key))

        add_items(project_id, self.project_structure, self.project_folder_path)

    def add_parsed_file_to_tree(self, parent_id):
        # Add imports to the treeview
        imports_id = self.tree.insert(parent_id, "end", text="Imports", tags=("key",))
        for imp in self.analyzer.imports:
            self.tree.insert(imports_id, "end", text=imp)

        # Add classes, properties, and methods to the treeview
        for cls, details in self.analyzer.classes.items():
            class_id = self.tree.insert(
                parent_id, "end", text=f"Class: {cls}", tags=("key",)
            )
            self.tree.insert(
                class_id, "end", text=f"Bases: {', '.join(details['bases'])}"
            )
            if details.get("docstring"):
                self.tree.insert(
                    class_id, "end", text=f"Docstring: {details['docstring']}"
                )

            properties_id = self.tree.insert(
                class_id, "end", text="Properties", tags=("key",)
            )
            for prop in details["properties"]:
                self.tree.insert(properties_id, "end", text=prop, tags=("property",))

            methods_id = self.tree.insert(
                class_id, "end", text="Methods", tags=("key",)
            )
            for method in details["methods"]:
                method_id = self.tree.insert(
                    methods_id,
                    "end",
                    text=f"Method: {method['name']}",
                    tags=("method", "bold"),
                )
                self.tree.insert(
                    method_id, "end", text=f"Args: {', '.join(method['args'])}"
                )
                if method["returns"]:
                    self.tree.insert(
                        method_id, "end", text=f"Returns: {method['returns']}"
                    )
                if method.get("docstring"):
                    self.tree.insert(
                        method_id, "end", text=f"Docstring: {method['docstring']}"
                    )

        # Add standalone functions to the treeview
        functions_id = self.tree.insert(
            parent_id, "end", text="Functions", tags=("key",)
        )
        for func in self.analyzer.functions:
            func_id = self.tree.insert(
                functions_id,
                "end",
                text=f"Function: {func['name']}",
                tags=("method", "bold"),
            )
            self.tree.insert(
                func_id,
                "end",
                text=f"Args: {', '.join(func['args'])}",
                tags=("method",),
            )
            if func["returns"]:
                self.tree.insert(
                    func_id, "end", text=f"Returns: {func['returns']}", tags=("method",)
                )
            if func.get("docstring"):
                self.tree.insert(
                    func_id,
                    "end",
                    text=f"Docstring: {func['docstring']}",
                    tags=("method",),
                )

    def on_closing(self):
        # Close the database connection before exiting
        self.conn.close()
        self.destroy()


if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
