# src/core/data_processing.py

def filter_wm_group_data(wm_group_data, filter_criteria):
    # Process and return filtered data based on some criteria
    return {k: v for k, v in wm_group_data.items() if filter_criteria in k}