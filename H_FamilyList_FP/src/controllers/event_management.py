# src/controllers/event_management.py


def handle_tab_click(event, notebook, state):
    """Handle a tab click event."""
    clicked_tab_index = notebook.index("@%d,%d" % (event.x, event.y))
    clicked_tab_name = notebook.tab(clicked_tab_index, "text")

    # Log the clicked tab name
    logging_text_widget = state.logging_text_widget
    # logging_text_widget.write(f"Clicked on tab: {clicked_tab_name}\n")
    logging_text_widget.write(f":: [ {clicked_tab_name} ] 탭에 오셨습니다. ::\n")

    # Set the clicked tab in the state (optional)
    state.set_current_tab(clicked_tab_name)

