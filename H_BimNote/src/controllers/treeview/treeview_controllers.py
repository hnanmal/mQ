from src.controllers.event_controllers import dispatch_event
from src.controllers.clipboard_management import (
    copy_to_clipboard,
    paste_external_data,
    paste_from_clipboard,
)
from src.views.context_menu import generate_context_menu
from src.views.dialogs import ask_paste_location
from src.views.styles import configure_tree_styles
from src.views.treeview.tree_tag_manage import determine_tag_by_level


def on_item_select(event, state):
    logging_text_widget = state.logging_text_widget
    tree = event.widget
    selected_item = tree.selection()[0]
    dispatch_event(
        "ITEM_SELECT",
        state,
        {"tree": tree, "item": selected_item, "logging_widget": logging_text_widget},
    )


def on_right_click(event, state, tree):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if item and column:
        menu = generate_context_menu(state, tree, item, column)
        menu.post(event.x_root, event.y_root)


def handle_copy(tree, event, state):
    try:
        selected_items = tree.selection()
        # 디버깅: 선택된 항목 확인
        print(f"Selected items for copy: {selected_items}")

        if selected_items:
            copy_to_clipboard(tree, selected_items, state)
            print(f"Items copied: {selected_items}")
    except Exception as e:
        print(f"Error during copy: {e}")


def handle_paste(tree, event, state):
    clipboard_data = state.get_clipboard_data()
    # 상태 객체에서 클립보드 데이터를 가져옴
    print(f"Clipboard data before paste: {clipboard_data}")

    selected_items = tree.selection()
    print(f"selected_items: {selected_items}")

    # 트리뷰 복사 및 붙여넣기 처리
    if selected_items:
        if clipboard_data:  # 클립보드에 트리뷰 데이터가 있는지 확인
            print("Pasting within TreeView")  # 디버깅 라인
            # paste_from_clipboard(tree, selected_items[0])
            for target_item in selected_items:
                paste_from_clipboard(tree, selected_items, clipboard_data)
        else:
            # 외부 소스에서 데이터 붙여넣기
            print("Pasting from external source")  # 디버깅 라인
            paste_target_items = selected_items
            paste_to = (
                ask_paste_location()
            )  # 붙여넣기 위치 선택 (Name 또는 Description)
            if paste_to:
                paste_external_data(tree, paste_target_items, paste_to)


search_state = {"last_search": None, "last_match": None}


def get_clicked_column(tree, event):
    """Determine which column was clicked based on x-coordinate."""
    return tree.identify_column(event.x)


def search_treeview(tree, search_text):
    """Search the Treeview for items that match the search_text in the Name or Description."""
    global search_state
    items = tree.get_children("")

    # Flatten the tree to get a list of all items
    all_items = []

    def flatten_tree(parent):
        for item in tree.get_children(parent):
            all_items.append(item)
            flatten_tree(item)

    flatten_tree("")

    # If continuing from the last search, start after the last matched item
    start_index = 0
    if (
        search_state["last_search"] == search_text
        and search_state["last_match"] is not None
    ):
        start_index = all_items.index(search_state["last_match"]) + 1

    # Search for the next match
    for i in range(start_index, len(all_items)):
        item = all_items[i]
        item_values = tree.item(item, "values")
        item_name = item_values[0] if len(item_values) > 0 else ""
        item_description = item_values[1] if len(item_values) > 1 else ""

        if (
            search_text.lower() in item_name.lower()
            or search_text.lower() in item_description.lower()
        ):
            tree.selection_set(item)
            tree.see(item)
            search_state["last_search"] = search_text
            search_state["last_match"] = item
            return

    # If no match is found or the end of the tree is reached, reset the search
    search_state["last_search"] = None
    search_state["last_match"] = None
    print("No more matches found.")


def populate_treeview(tree, data, parent="", level=0):
    """Populate the Treeview widget with JSON data."""

    def insert_items(parent, items, level):
        for item in items:
            # Determine the appropriate tag based on the level
            tag = determine_tag_by_level(level)

            # Add indentation based on the level
            indented_name = "  " * level + item["name"]
            node_id = tree.insert(
                parent,
                "end",
                text=item["number"],
                values=(indented_name, item.get("description", "")),
                tags=(tag,),
            )
            children = item.get("children", [])
            if children:
                insert_items(node_id, children, level + 1)

    tree.delete(*tree.get_children())  # Clear the existing tree view
    insert_items(parent, data, level)

    # Force a refresh to apply styles
    configure_tree_styles(tree)
    tree.update_idletasks()


def expand_or_collapse_tree(tree, level):
    """Expand or collapse tree view items up to the specified level."""

    def expand_children(item, current_level, target_level):
        if current_level < target_level:
            tree.item(item, open=True)
            children = tree.get_children(item)
            for child in children:
                expand_children(child, current_level + 1, target_level)
        else:
            tree.item(item, open=False)

    root_items = tree.get_children("")
    for item in root_items:
        expand_children(item, 1, level)

    configure_tree_styles(tree)
    tree.update_idletasks()
