# -*- coding: utf-8 -*-

"""Print name, area, and perimeter of all rooms in the model."""

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *

import revit_script_util
from revit_script_util import Output

doc = revit_script_util.GetScriptDocument()

rooms = (
    FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_Rooms)
    .WhereElementIsNotElementType()
    .ToElements()
)

Output("🔍 전체 Room 개수: {}".format(len(rooms)))

for room in rooms:
    name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    area = room.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble()
    perimeter = room.get_Parameter(BuiltInParameter.ROOM_PERIMETER).AsDouble()

    sqft_to_sqm = 0.092903
    ft_to_m = 0.3048
    area_sqm = round(area * sqft_to_sqm, 2)
    perimeter_m = round(perimeter * ft_to_m, 2)

    Output("📌 Room: {} | 면적: {} ㎡ | 둘레: {} m".format(name, area_sqm, perimeter_m))
