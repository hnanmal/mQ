from src.tabs.familyType_manage_tab.utils import update_selected_calcType


def update_combobox_data_other(state, data, tab_name=None):
    """
    Update the combobox values based on the data loaded from the JSON file.
    """
    #####################
    #### building combobox
    bd_combobox = state[tab_name]["bd_combobox"]

    building_items = data.get("building_list", [])
    building_names = list(map(lambda x: x["building_name"], building_items))

    # Update the combobox values
    bd_combobox["values"] = ["프로젝트 공통"] + building_names

    # Set the default value to the first item if available
    if building_names and state.selected_building != "대상 빌딩 선택":
        bd_combobox.set(state.selected_building)
        print(type(state.selected_building))
        print(state.selected_building)
        pass
    elif building_names and not state.selected_building:
        bd_combobox.set("대상 빌딩 선택")
    else:
        bd_combobox.set("")  # Clear the combobox if no items are available

    #####################
    ### calc combobox
    calc_combobox = state[tab_name]["calc_comboBox"]
    calc_items = data.get("calc_types", [])
    calcType_names = list(
        map(
            lambda x: x["type_tag"],
            filter(lambda x: x["category"] == tab_name, calc_items),
        )
    )

    # Update the combobox values
    calc_combobox["values"] = calcType_names

    # Set the default value to the first item if available
    if calcType_names:
        calc_combobox.set(calcType_names[0])
    else:
        calc_combobox.set("")  # Clear the combobox if no items are available


def update_stdTypeTree_otherCat(event, state, tab_name, mode=None):
    bd_comboBox = state[tab_name]["bd_combobox"]
    state.selected_building = bd_comboBox.get()
    print(type(state.selected_building))
    print(state.selected_building)

    update_selected_calcType(
        event,
        state,
        state[tab_name]["calc_comboBox"],
        state[tab_name]["selected_calcType_label"],
        state[tab_name]["selected_calcType_sheetview"],
    )

    def find_stdType_items_inCat(cat, state):
        def find_level_5_items(
            node,
            level=1,
        ):
            # Initialize an empty list to store level 5 items
            level_5_items = []

            # Check if the current node is a level 5 item by counting dots in 'number'
            if node.get("number", "").count(".") == 4:
                level_5_items.append(
                    {
                        "name": node.get("name"),
                        "number": node.get("number"),
                        "description": node.get("description"),
                    }
                )

            # If the node has children, iterate over them and recurse
            if "children" in node:
                for child in node["children"]:
                    level_5_items.extend(find_level_5_items(child, level + 1))

            return level_5_items

        lv_5_items = []
        for root_node in state.stdTypes_info:
            if root_node["name"] == cat:
                lv_5_items.extend(find_level_5_items(root_node))
        state.project_info["std_types"] = list(
            map(
                lambda x: {
                    "std_type": x["name"],
                    "building_tag": "",
                },
                lv_5_items,
            )
        )
        return lv_5_items

    if not state.project_info.get("std_types"):
        find_stdType_items_inCat(tab_name, state)

    stdType_items = state.project_info["std_types"]

    if mode == "loading" and not state.selected_stdType:
        state[tab_name]["stdTypeTree"].delete(
            *state[tab_name]["stdTypeTree"].get_children()
        )

        for dic in stdType_items:
            print(dic)
            state[tab_name]["stdTypeTree"].insert("", "end", values=list(dic.values()))
    # elif selected_building and selected_stdType:
    #     state.stdTypeTree_inRoom.selection_set(state.selected_stdType)
    #     pass
