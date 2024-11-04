import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
from tksheet import Sheet
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re


class FunctionManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Function Manager")
        self.root.geometry("1600x800")

        # Data Storage
        self.functions_data = []
        self.dependency_graph = nx.DiGraph()

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Paned Window for resizing frames
        paned_window = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        paned_window.grid(row=0, column=0, sticky="nsew")

        # Frame for function input fields
        input_frame = ttk.LabelFrame(paned_window, text="Add Function/Class Details")
        paned_window.add(input_frame, weight=1)

        # Function fields
        labels = [
            "Module Name",
            "Class Name",
            "Function Name",
            "Description",
            "Inputs",
            "Outputs",
            "Class Properties",
            "Class Methods",
            "Composed Classes",
            "Referenced Classes",
        ]
        self.entries = {}
        for idx, label in enumerate(labels):
            ttk.Label(input_frame, text=label).grid(
                row=idx, column=0, sticky="w", padx=5, pady=2
            )
            entry = ttk.Entry(input_frame, width=50)
            entry.grid(row=idx, column=1, padx=5, pady=2, sticky="ew")
            self.entries[label] = entry

        # Add Function/Class Button
        add_button = ttk.Button(
            input_frame, text="Add Function/Class", command=self.add_function
        )
        add_button.grid(row=len(labels), column=1, pady=5, sticky="e")

        # Auto Parse Button
        parse_button = ttk.Button(
            input_frame, text="Auto Parse Code", command=self.auto_parse_function
        )
        parse_button.grid(row=len(labels), column=0, pady=5, sticky="w")

        # Text widget for Auto Parse Code
        self.auto_parse_text = tk.Text(input_frame, height=10, width=50)
        self.auto_parse_text.grid(
            row=len(labels) + 1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )

        # Frame for tksheet and canvas
        main_frame = ttk.Frame(paned_window)
        paned_window.add(main_frame, weight=3)

        # Paned Window inside main_frame for sheet and canvas
        main_paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill="both", expand=True, padx=10, pady=10)

        # tksheet to display functions/classes
        sheet_frame = ttk.Frame(main_paned)
        main_paned.add(sheet_frame, weight=2)

        self.sheet = Sheet(
            sheet_frame,
            headers=[
                "Module Name",
                "Class Name",
                "Function Name",
                "Description",
                "Inputs",
                "Outputs",
                "Class Properties",
                "Class Methods",
                "Composed Classes",
                "Referenced Classes",
            ],
            height=300,
        )
        self.sheet.pack(fill="both", expand=True)

        # Bind selection event to display class details
        self.sheet.enable_bindings("cell_select")
        self.sheet.bind("<ButtonRelease-1>", self.display_class_details)

        # Canvas for dependency graph
        canvas_frame = ttk.Frame(main_paned)
        main_paned.add(canvas_frame, weight=1)

        self.figure = plt.Figure(figsize=(7, 5))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=canvas_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Frame for relationship diagram
        diagram_frame = ttk.Frame(paned_window)
        paned_window.add(diagram_frame, weight=1)

        self.diagram_canvas = FigureCanvasTkAgg(self.figure, master=diagram_frame)
        self.diagram_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Frame for additional buttons
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        save_button = ttk.Button(
            button_frame, text="Save to JSON", command=self.save_to_json
        )
        save_button.pack(side="left")

        load_button = ttk.Button(
            button_frame, text="Load from JSON", command=self.load_from_json
        )
        load_button.pack(side="left", padx=5)

        move_button = ttk.Button(
            button_frame, text="Move Function/Class", command=self.move_function
        )
        move_button.pack(side="left", padx=5)

        edit_button = ttk.Button(
            button_frame, text="Edit Selected Row", command=self.edit_function
        )
        edit_button.pack(side="left", padx=5)

        # Class Details Widget
        self.class_details_label = tk.Label(
            self.root, text="", font=("Arial", 16), anchor="e", justify="right"
        )
        self.class_details_label.grid(row=0, column=1, sticky="ne", padx=20, pady=10)

        # Configure grid weights to make widgets responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=3)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        input_frame.grid_rowconfigure(len(labels) + 1, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)
        sheet_frame.grid_rowconfigure(0, weight=1)
        sheet_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.update_canvas()

    def add_function(self):
        # Get data from entry fields
        function_details = {label: self.entries[label].get() for label in self.entries}

        # Add to sheet and internal data list
        self.functions_data.append(function_details)
        self.sheet.insert_rows(1)  # Add one empty row at the end if no row exists
        current_total_rows = self.sheet.get_total_rows()
        for col_idx, value in enumerate(function_details.values()):
            self.sheet.set_cell_data(current_total_rows - 1, col_idx, value)

        # Update dependency graph
        function_name = function_details.get(
            "Function Name", ""
        ) or function_details.get("Class Name", "")
        self.dependency_graph.add_node(function_name, **function_details)

        # Add composition and reference relationships
        composed_classes = function_details.get("Composed Classes").split(",")
        referenced_classes = function_details.get("Referenced Classes").split(",")
        for class_name in composed_classes:
            if class_name.strip():
                self.dependency_graph.add_edge(
                    function_name, class_name.strip(), type="composition"
                )
        for class_name in referenced_classes:
            if class_name.strip():
                self.dependency_graph.add_edge(
                    function_name, class_name.strip(), type="reference"
                )

        # Clear input fields
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        # Update the canvas
        self.update_canvas()

    def auto_parse_function(self):
        # Automatically parse a function or class code from user input
        code = self.auto_parse_text.get("1.0", "end-1c")
        if not code:
            return

        # Extract details from the pasted code
        function_details = {
            "Module Name": "Unknown Module",
            "Class Name": "",
            "Function Name": "",
            "Description": "",
            "Inputs": "",
            "Outputs": "",
            "Class Properties": "",
            "Class Methods": "",
            "Composed Classes": "",
            "Referenced Classes": "",
        }

        # Use regex to parse function or class name
        class_match = re.search(r"class\s+(\w+)\s*:", code)
        if class_match:
            # It is a class
            class_name = class_match.group(1)
            function_details["Class Name"] = class_name

            # Extract class properties
            properties_match = re.findall(r"self\.(\w+)\s*=", code)
            function_details["Class Properties"] = ", ".join(properties_match)

            # Extract class methods
            methods_match = re.findall(r"def\s+(\w+)\s*\(", code)
            # Filter out the __init__ method if present
            methods_match = [method for method in methods_match if method != "__init__"]
            function_details["Class Methods"] = ", ".join(methods_match)

        else:
            # It is a function
            function_match = re.search(r"def\s+(\w+)\s*\(", code)
            if function_match:
                function_details["Function Name"] = function_match.group(1)

            # Extract inputs
            inputs_match = re.search(r"def\s+\w+\s*\(([^)]*)\)", code)
            if inputs_match:
                function_details["Inputs"] = inputs_match.group(1)

        # Add to sheet and internal data list
        self.functions_data.append(function_details)
        self.sheet.insert_rows(1)  # Add one empty row at the end if no row exists
        current_total_rows = self.sheet.get_total_rows()
        for col_idx, value in enumerate(function_details.values()):
            self.sheet.set_cell_data(current_total_rows - 1, col_idx, value)

        # Update dependency graph
        function_name = function_details.get(
            "Function Name", ""
        ) or function_details.get("Class Name", "")
        self.dependency_graph.add_node(function_name, **function_details)

        # Clear input fields
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        # Update the canvas
        self.update_canvas()

    def save_to_json(self):
        # Save functions data to JSON file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(self.functions_data, file, indent=4, ensure_ascii=False)
                messagebox.showinfo("Success", "Data saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_from_json(self):
        # Load functions data from JSON file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.functions_data = json.load(file)
                self.refresh_sheet()
                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def refresh_sheet(self):
        # Clear and refresh the sheet with loaded data
        self.sheet.set_sheet_data(
            [[func[key] for key in func] for func in self.functions_data]
        )

        # Refresh dependency graph
        self.dependency_graph.clear()
        for function in self.functions_data:
            function_name = function.get("Function Name", "") or function.get(
                "Class Name", ""
            )
            self.dependency_graph.add_node(function_name, **function)
            composed_classes = function.get("Composed Classes", "").split(",")
            referenced_classes = function.get("Referenced Classes", "").split(",")
            for class_name in composed_classes:
                if class_name.strip():
                    self.dependency_graph.add_edge(
                        function_name, class_name.strip(), type="composition"
                    )
            for class_name in referenced_classes:
                if class_name.strip():
                    self.dependency_graph.add_edge(
                        function_name, class_name.strip(), type="reference"
                    )

        # Update the canvas
        self.update_canvas()

    def update_canvas(self):
        # Update the dependency graph on the canvas
        self.ax.clear()
        if len(self.dependency_graph.nodes) == 0:
            self.ax.set_title("No functions or classes to analyze.")
        else:
            pos = nx.spring_layout(self.dependency_graph)

            # Draw functions and modules
            for node in self.dependency_graph.nodes(data=True):
                label = node[0]
                module_name = node[1].get("Module Name", "Unknown Module")
                if node[1].get("Class Name"):
                    nx.draw_networkx_nodes(
                        self.dependency_graph,
                        pos,
                        nodelist=[node[0]],
                        node_shape="o",
                        ax=self.ax,
                        node_color="lightblue",
                        node_size=500,
                    )
                else:
                    nx.draw_networkx_nodes(
                        self.dependency_graph,
                        pos,
                        nodelist=[node[0]],
                        node_shape="s",
                        ax=self.ax,
                        node_color="lightgreen",
                        node_size=500,
                    )
                nx.draw_networkx_labels(
                    self.dependency_graph,
                    pos,
                    labels={node[0]: f"{module_name}\n{label}"},
                    font_size=8,
                    ax=self.ax,
                )

            # Draw different types of edges
            edges = nx.get_edge_attributes(self.dependency_graph, "type")
            composition_edges = [e for e in edges if edges[e] == "composition"]
            reference_edges = [e for e in edges if edges[e] == "reference"]
            nx.draw_networkx_edges(
                self.dependency_graph,
                pos,
                edgelist=composition_edges,
                ax=self.ax,
                edge_color="green",
                label="Composition",
            )
            nx.draw_networkx_edges(
                self.dependency_graph,
                pos,
                edgelist=reference_edges,
                ax=self.ax,
                edge_color="red",
                label="Reference",
            )

            self.ax.legend()
            self.ax.set_title("Class and Function Relationships")

        self.canvas.draw()

    def move_function(self):
        # Move a function from one module to another
        selected_row = self.sheet.get_currently_selected()
        if not selected_row:
            messagebox.showwarning("Warning", "Please select a function to move.")
            return

        function_name = self.sheet.get_cell_data(
            selected_row[0], 2
        ) or self.sheet.get_cell_data(selected_row[0], 1)
        new_module = simpledialog.askstring(
            "Move Function/Class",
            f"Enter new module for function/class '{function_name}':",
        )
        if new_module:
            for function in self.functions_data:
                if (
                    function["Function Name"] == function_name
                    or function["Class Name"] == function_name
                ):
                    function["Module Name"] = new_module
                    self.refresh_sheet()
                    break

    def edit_function(self):
        # Edit the details of the selected function/class
        selected_row = self.sheet.get_currently_selected()
        if not selected_row:
            messagebox.showwarning("Warning", "Please select a function to edit.")
            return

        # Get the current details
        current_details = {
            label: self.sheet.get_cell_data(selected_row[0], idx)
            for idx, label in enumerate(self.entries.keys())
        }

        # Populate the entry fields with current details
        for label, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, current_details[label])

        # Update function
        def save_changes():
            updated_details = {
                label: self.entries[label].get() for label in self.entries
            }
            for idx, value in enumerate(updated_details.values()):
                self.sheet.set_cell_data(selected_row[0], idx, value)
            self.functions_data[selected_row[0]] = updated_details
            self.refresh_sheet()
            edit_window.destroy()

        # Create a new window for editing
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Function/Class")
        edit_window.geometry("600x600")

        for idx, label in enumerate(self.entries.keys()):
            ttk.Label(edit_window, text=label).grid(
                row=idx, column=0, sticky="w", padx=5, pady=2
            )
            entry = ttk.Entry(edit_window, width=50)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            entry.insert(0, current_details[label])
            self.entries[label] = entry

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.grid(row=len(self.entries), column=1, pady=5, sticky="e")

    def display_class_details(self, event):
        # Display the class details in the label widget when a row is selected
        selected_row = self.sheet.get_currently_selected()
        if selected_row:
            class_name = self.sheet.get_cell_data(
                selected_row[0], 1
            ) or self.sheet.get_cell_data(selected_row[0], 2)
            class_properties = self.sheet.get_cell_data(selected_row[0], 6)
            self.class_details_label.config(
                text=f"Class Name: {class_name}\nProperties: {class_properties}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionManagerApp(root)
    root.mainloop()
