def convert_SGWMsheet_data_to_dict(sheet_data):
    sheet_data_dict = {}
    current_parent = None
    current_sub_parent = None

    for row in sheet_data:
        if row[0]:  # Top-level parent
            current_parent = row[0]
            sheet_data_dict[current_parent] = {}
        elif row[1]:  # Sub-level parent
            current_sub_parent = row[1]
            sheet_data_dict[current_parent][current_sub_parent] = []
        elif row[2]:  # Children
            sheet_data_dict[current_parent][current_sub_parent].append(row[2])

    return sheet_data_dict


# def convert_dict_to_SGWMsheet_data(sheet_data_dict):
#     sheet_data = []

#     for parent, sub_dict in sheet_data_dict.items():
#         # 최상위 항목을 리스트에 추가
#         sheet_data.append([parent, None, None])
#         for sub_parent, children in sub_dict.items():
#             # 중간 항목을 리스트에 추가
#             sheet_data.append([None, sub_parent, None])
#             for child in children:
#                 # 하위 항목들을 리스트에 추가
#                 sheet_data.append([None, None, child])

#     return sheet_data


def convert_dict_to_SGWMsheet_data(sheet_data_dict):
    sheet_data = []

    for parent, sub_dict in sheet_data_dict.items():
        # 최상위 항목을 리스트에 추가
        sheet_data.append([parent, None, None])
        for sub_parent, children in sub_dict.items():
            # 중간 항목을 리스트에 추가
            # sheet_data.append([None, sub_parent, None])
            for idx, child in enumerate(children):
                # 하위 항목들을 리스트에 추가
                if idx == 0:
                    sheet_data.append([None, sub_parent, child])
                elif idx == len(children) - 1:
                    sheet_data.append([None, None, child])
                    sheet_data.append([None, None, None])
                else:
                    sheet_data.append([None, None, child])

    return sheet_data


def parse_sheet_toJson(sheet, mode=None):
    _sheet_data = sheet.get_sheet_data()
    if not mode:
        mode = sheet.kind

    if mode == "std-GWM":
        res = convert_SGWMsheet_data_to_dict(_sheet_data)

    return res


def parse_Json_toSheet(jsonData, mode=None):
    if mode == "std-GWM":
        res = convert_dict_to_SGWMsheet_data(jsonData)

    return res
