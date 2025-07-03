import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Solid, Face, PlanarFace

from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

stairs = UnwrapElement(IN[0])


def find_A_Landing(stair):
    stair = UnwrapElement(stair)
    options = Options()
    total_area_m2 = 0.0

    # 1. Get landing elements
    landing_ids = stair.GetStairsLandings()
    landings = [doc.GetElement(lid) for lid in landing_ids]

    # 2. Loop through each landing geometry
    for landing in landings:
        geom = landing.get_Geometry(options)
        for solid in geom:
            if not isinstance(solid, Solid):
                continue
            for face in solid.Faces:
                # 3. Only use horizontal (upward-facing) planar faces
                if isinstance(face, PlanarFace):
                    normal = face.FaceNormal
                    if abs(normal.Z - 1.0) < 0.01:  # Z+ 방향이면 수평면
                        total_area_m2 += face.Area * 0.092903  # ft² → m²

    res = total_area_m2
    return res


OUT = map(find_A_Landing, stairs)
