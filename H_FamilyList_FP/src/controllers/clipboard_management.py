# clipboard_management.py

clipboard_data = []

def copy_to_clipboard(items):
    global clipboard_data
    clipboard_data = items
    print(f"Copied {len(items)} items to clipboard")

def paste_from_clipboard():
    global clipboard_data
    return clipboard_data if clipboard_data else None

def paste_copied_items(destination, clipboard_items):
    # Example implementation: Append items to the destination list
    for item in clipboard_items:
        destination.append(item)
    print(f"Pasted {len(clipboard_items)} items to destination")
