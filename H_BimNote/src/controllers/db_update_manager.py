# src/controllers/db_update_manager.py


class DBUpdateManager:
    def __init__(self, state):
        self.state = state

    def update_state_from_widget(self, widget_type, widget, data):
        """
        General function to update the state from different widget types.
        """
        if widget_type == "listbox":
            self._update_state_from_listbox(widget, data)
        elif widget_type == "tksheet":
            self._update_state_from_tksheet(widget, data)
        elif widget_type == "treeview":
            self._update_state_from_treeview(widget, data)
        else:
            print(f"Unknown widget type: {widget_type}")

    def _update_state_from_listbox(self, listbox, data):
        # Assuming listbox data structure to update the state
        self.state["listbox_data"] = data

    def _update_state_from_tksheet(self, sheet, data):
        # Convert the sheet data into a dictionary and update the state
        sheet_data_dict = self.convert_sheet_data_to_dict(data)
        self.state["sheet_data"] = sheet_data_dict

    def _update_state_from_treeview(self, tree, data):
        # Convert the treeview data into a dictionary and update the state
        tree_data_dict = self.convert_tree_data_to_dict(data)
        self.state["tree_data"] = tree_data_dict

    def convert_sheet_data_to_dict(self, sheet_data):
        """
        Convert tksheet data into a nested dictionary.
        """
        new_db = {}

        current_parent = None
        current_sub_parent = None

        for row in sheet_data:
            if row[0]:  # Top-level parent
                current_parent = row[0]
                new_db[current_parent] = {}
            elif row[1]:  # Sub-level parent
                current_sub_parent = row[1]
                new_db[current_parent][current_sub_parent] = []
            elif row[2]:  # Children
                new_db[current_parent][current_sub_parent].append(row[2])

        return new_db

    def find_and_update_item_in_state(self, parent, sub_parent, new_name):
        """
        Find and update an existing item in the nested dictionary.
        """
        if parent in self.state["sheet_data"]:
            if sub_parent in self.state["sheet_data"][parent]:
                # Update the item in the sub_parent
                items = self.state["sheet_data"][parent][sub_parent]
                for index, item in enumerate(items):
                    if item == new_name:
                        # Update or modify as necessary
                        self.state["sheet_data"][parent][sub_parent][index] = new_name

    def update_item_name_in_tksheet(self, sheet, old_name, new_name):
        """
        Update the name of an item in tksheet.
        """
        sheet_data = sheet.get_sheet_data(return_copy=True)
        for row_index, row in enumerate(sheet_data):
            if old_name in row:
                col_index = row.index(old_name)
                sheet_data[row_index][col_index] = new_name
                break
        # Update the tksheet with modified data
        sheet.set_sheet_data(sheet_data)
