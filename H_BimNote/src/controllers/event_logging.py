def log_event_selection(tree, item, logging_widget):
    """Log the details of a tree item to the logging area."""
    item_text = tree.item(item, "text")
    item_values = tree.item(item, "values")

    # Retrieve the tags associated with the item
    item_tags = tree.item(item, "tags")

    # Prepare the log message
    log_message = f"Selected Item:\nNumber: {item_text}\n"

    if item_tags:
        log_message += f"Tags: {', '.join(item_tags)}\n"

    if item_values:
        log_message += f"Name: {item_values[0]}\nDescription: {item_values[1]}\n"

    # Write the log message to the logging widget
    logging_widget.write(log_message)


def log_event_add(tree, item, logging_widget):
    """Log the details of a tree item to the logging area."""
    item_text = tree.item(item, "text")
    item_values = tree.item(item, "values")

    # Retrieve the tags associated with the item
    item_tags = tree.item(item, "tags")

    # Prepare the log message
    log_message = f"Added Item:\nNumber: {item_text}\n"

    if item_tags:
        log_message += f"Tags: {', '.join(item_tags)}\n"

    if item_values:
        log_message += f"Name: {item_values[0]}\nDescription: {item_values[1]}\n"

    # Write the log message to the logging widget
    logging_widget.write(log_message)


def log_event_remove(tree, item, logging_widget):
    """Log the details of a tree item to the logging area."""
    for item_id in item:  # Handle all items if multiple
        item_text = tree.item(item_id, "text")
        item_values = tree.item(item_id, "values")
        item_tags = tree.item(item_id, "tags")

        # Prepare the log message
        log_message = f"Removed Item:\nNumber: {item_text}\n"
        if item_tags:
            log_message += f"Tags: {', '.join(item_tags)}\n"
        if item_values:
            log_message += f"Name: {item_values[0]}\nDescription: {item_values[1]}\n"

        # Write the log message to both the terminal and the logging widget
        logging_widget.write(log_message)
