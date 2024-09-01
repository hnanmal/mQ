# src/views/rendering.py

def render_treeview(tree, data):
    for item in data:
        tree.insert("", "end", text=item["item_name"], values=item["matched_data"])

def update_treeview_style(tree, lock_status):
    for item in tree.get_children():
        item_name = tree.item(item, "text")
        if lock_status.get(item_name):
            tree.item(item, tags=("locked",))
        else:
            tree.item(item, tags=("unlocked",))

    tree.tag_configure("locked", background="gray")
    tree.tag_configure("unlocked", background="white")