import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Solid, GeometryInstance, PlanarFace, ViewDetailLevel

from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

stairs = UnwrapElement(IN[0])


def get_support_elements(run):
    support_elems = []
    for ref_id in run.GetLeftSupports() + run.GetRightSupports():
        elem = doc.GetElement(ref_id)
        if elem:
            support_elems.append(elem)
    return support_elems


def find_SA_Stringer(stair):
    stair = UnwrapElement(stair)
    FT2_TO_M2 = 0.092903
    total_area_m2 = 0.0
    options = Options()
    options.DetailLevel = ViewDetailLevel.Fine
    options.IncludeNonVisibleObjects = True

    run_ids = stair.GetStairsRuns()
    runs = [doc.GetElement(rid) for rid in run_ids]

    for run in runs:
        supports = get_support_elements(run)

        for support in supports:
            geom = support.get_Geometry(options)
            if not geom:
                continue

            solids = []
            for g in geom:
                if isinstance(g, Solid) and g.Faces.Size > 0:
                    solids.append(g)
                elif isinstance(g, GeometryInstance):
                    for sg in g.GetInstanceGeometry():
                        if isinstance(sg, Solid) and sg.Faces.Size > 0:
                            solids.append(sg)

            for solid in solids:
                for face in solid.Faces:
                    total_area_m2 += face.Area * FT2_TO_M2

    return total_area_m2


OUT = list(map(find_SA_Stringer, stairs))
