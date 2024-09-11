# # Load Project Info Button
# def load_project_info():
#     file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
#     if file_path:
#         with open(file_path, "r", encoding="utf-8") as f:
#             loaded_data = json.load(f)

#         # Save loaded data to state
#         state["project_info"] = loaded_data

#         # Populate UI fields from project_info
#         project_name_var.set(loaded_data.get("project_name", ""))
#         project_type_var.set(loaded_data.get("project_type", ""))

#         # Clear and populate the building treeview
#         building_treeview.delete(*building_treeview.get_children())
#         for building_name, building_data in loaded_data.get(
#             "building_list", {}
#         ).items():
#             building_treeview.insert(
#                 "",
#                 "end",
#                 values=(
#                     building_data["building_name"],
#                     building_data["building_number"],
#                 ),
#             )

#         # Clear and populate finish types for the selected building
#         finish_listbox.delete(0, tk.END)
#         selected_building = building_treeview.selection()
#         if selected_building:
#             selected_building_name = building_treeview.item(
#                 selected_building[0], "values"
#             )[0]
#             finish_types = (
#                 loaded_data.get("building_list", {})
#                 .get(selected_building_name, {})
#                 .get("finish_types", [])
#             )
#             for finish_type in finish_types:
#                 finish_listbox.insert(tk.END, finish_type)

#         print(f"Project Info loaded from {file_path}")