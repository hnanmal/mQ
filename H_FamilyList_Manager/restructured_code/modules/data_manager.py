# modules/data_manager.py

import json

def load_wm_group_match_data(app):
    try:
        with open("wm_group_match.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Load the lock status from the JSON file
        app.lock_status = data.get("lock_status", {})

        # Ensure the treeview is already initialized before trying to access it
        if hasattr(app, 'wm_group_treeview'):
            for item in app.wm_group_treeview.get_children():
                item_name = app.wm_group_treeview.item(item, "values")[0]
                is_locked = app.lock_status.get(item_name, False)
                if is_locked:
                    app.wm_group_treeview.item(item, tags=("locked",))
                else:
                    app.wm_group_treeview.item(item, tags=("unlocked",))

        return data
    except FileNotFoundError:
        app.lock_status = {}
        return {}


def save_wm_group_match_data(data):
    with open("wm_group_match.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
