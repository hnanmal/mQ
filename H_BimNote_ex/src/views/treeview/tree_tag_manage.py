def determine_tag_by_level(level):
    """Determine the appropriate tag based on the level of the TreeView item."""
    lv_1st = 0
    lv_2nd = 4

    if level == lv_1st:
        return f"Level{lv_1st}"
    elif level == lv_2nd:
        return f"Level{lv_2nd}"
    else:
        return "OtherLevels"
