# src/models/sheet_utils.py

import src.core.fp_utils


def convert_SGWMsheet_data_to_dict(state, sheet_data):
    if state.team_std_info.get("std-GWM"):
        # db = state.team_std_info.get("std-GWM")
        db = state.team_std_info["std-GWM"]
        new_db = {}

        current_parent = None
        current_sub_parent = None

        for row in sheet_data:
            if row[0]:
                current_parent = row[0]
                new_db[current_parent] = db[current_parent]
            elif row[1]:  # Sub-level parent
                current_sub_parent = row[1]
                # new_db[current_parent][current_sub_parent] = []
                new_db[current_parent][current_sub_parent].update(
                    db[current_parent][current_sub_parent][row[2]]
                )
            elif row[2]:  # Children
                # db[current_parent][current_sub_parent].append(row[2])
                new_db[current_parent][current_sub_parent].update(
                    db[current_parent][current_sub_parent][row[2]]
                )

    else:
        new_db = {}

        current_parent = None
        current_sub_parent = None

        for row in sheet_data:
            if row[0]:  # Top-level parent
                current_parent = row[0]
                new_db[current_parent] = {}
            elif row[1]:  # Sub-level parent
                current_sub_parent = row[1]
                new_db[current_parent][current_sub_parent] = []
                # db[current_parent][current_sub_parent].append(row[2])
                new_db[current_parent][current_sub_parent].append({row[2]: []})
            elif row[2]:  # Children
                # db[current_parent][current_sub_parent].append(row[2])
                new_db[current_parent][current_sub_parent].append({row[2]: []})

    return new_db


def convert_dict_to_SGWMsheet_data(db):
    sheet_data = []

    for parent, sub_dict in db.items():
        # 최상위 항목을 리스트에 추가
        sheet_data.append([parent, None, None])
        for sub_parent, children in sub_dict.items():
            # 중간 항목을 리스트에 추가
            # sheet_data.append([None, sub_parent, None])
            for idx, child in enumerate(children):
                # 하위 항목들을 리스트에 추가
                if idx == 0:
                    # sheet_data.append([None, sub_parent, list(child.keys())[0]])
                    sheet_data.append([None, sub_parent, child])
                elif idx == len(children) - 1:
                    sheet_data.append([None, None, child])
                    sheet_data.append([None, None, None])
                else:
                    sheet_data.append([None, None, child])

    return sheet_data


def parse_widget_toDB(state, sheet, mode=None):
    _sheet_data = sheet.get_sheet_data()
    if not mode:
        mode = sheet.kind

    if mode == "std-GWM":
        res = convert_SGWMsheet_data_to_dict(_sheet_data)

    return res


def parse_DB_toSheet(jsonData, mode=None):
    if mode == "std-GWM":
        res = convert_dict_to_SGWMsheet_data(jsonData)

    return res
