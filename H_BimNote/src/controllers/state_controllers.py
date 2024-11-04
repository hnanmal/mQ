def handle_tab_switch(state, new_tab_name):
    state.set_current_tab(new_tab_name)
    # Add any additional logic if needed


def handle_lock_toggle(state, item_name):
    current_status = state.get_lock_status(item_name)
    state.set_lock_status(item_name, not current_status)
    # Add additional logic to handle UI updates or data saving


def handle_tab_click(event, notebook, state):
    """Handle a tab click event."""
    clicked_tab_index = notebook.index("@%d,%d" % (event.x, event.y))
    # clicked_tab = notebook.tab(clicked_tab_index)
    clicked_tab_name = notebook.tab(clicked_tab_index, "text")
    state.clicked_tab_index = clicked_tab_index
    state.clicked_tab_name = clicked_tab_name
    # Log the clicked tab name
    logging_text_widget = state.logging_text_widget
    logging_text_widget.write(f":: [ {clicked_tab_name} ] 탭에 오셨습니다. ::\n")

    # # reload_tab_content(state, notebook) and remain current select building
    # update_combobox_data(state, state.bd_combobox_room, state.project_info, "building")
    # update_combobox_data(
    #     state, state.calc_comboBox_room, state.project_info, "calc", "Room"
    # )
    # update_combobox_data_other(state, state.project_info, "Floors")
    # update_combobox_data_other(state, state.project_info, "Roofs")

    # Set the clicked tab in the state (optional)
    state.set_current_tab(clicked_tab_name)
