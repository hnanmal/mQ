import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Solid, Face, PlanarFace

from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

stairs = UnwrapElement(IN[0])


def find_A_Tread(stair):
    stair = UnwrapElement(stair)
    from Autodesk.Revit.DB import GeometryInstance, Solid, PlanarFace, ViewDetailLevel

    options = Options()
    options.DetailLevel = ViewDetailLevel.Fine
    options.IncludeNonVisibleObjects = True

    total_area_m2 = 0.0
    run_ids = stair.GetStairsRuns()
    runs = [doc.GetElement(rid) for rid in run_ids]

    for run in runs:
        geom = run.get_Geometry(options)
        if not geom:
            continue
        for g in geom:
            solids = []
            # 직접 Solid인 경우
            if isinstance(g, Solid) and g.Faces.Size > 0:
                solids.append(g)
            # GeometryInstance 내부 파기
            elif isinstance(g, GeometryInstance):
                inst_geom = g.GetInstanceGeometry()
                for sub_geom in inst_geom:
                    if isinstance(sub_geom, Solid) and sub_geom.Faces.Size > 0:
                        solids.append(sub_geom)

            # 이제 solid 처리
            for solid in solids:
                for face in solid.Faces:
                    if isinstance(face, PlanarFace):
                        normal = face.FaceNormal
                        if normal.Z > 0.8:  # 상향 수평면
                            total_area_m2 += face.Area * 0.092903

    return total_area_m2


OUT = map(find_A_Tread, stairs)
