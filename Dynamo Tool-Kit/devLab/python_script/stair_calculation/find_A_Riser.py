import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

stairs = UnwrapElement(IN[0])


def find_A_Riser_from_properties(stair):
    stair = UnwrapElement(stair)
    FT2_TO_M2 = 0.092903
    total_area_m2 = 0.0

    run_ids = stair.GetStairsRuns()
    runs = [doc.GetElement(rid) for rid in run_ids]

    for run in runs:
        try:
            tread_width = run.get_ActualRunWidth()  # ft
            run_height = run.get_Height()  # ft
            tread_count = run.get_ActualTreadsNumber()  # int

            if None in [tread_width, run_height, tread_count] or tread_count == 0:
                continue

            # 전체 높이 / 디딤수 = Riser Height
            riser_height = run_height / tread_count

            area_ft2 = tread_width * riser_height * tread_count
            total_area_m2 += area_ft2 * FT2_TO_M2

        except:
            continue

    return total_area_m2


OUT = list(map(find_A_Riser_from_properties, stairs))
