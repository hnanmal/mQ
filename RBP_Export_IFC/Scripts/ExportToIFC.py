# -*- coding: utf-8 -*-
import clr
import os

# import System

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
# clr.AddReferenceToFileAndPath(r"D:\Program Files\Autodesk\Revit 2025\RevitAPIIFC.dll")
clr.AddReference(r"D:\Program Files\Autodesk\Revit 2025\RevitAPIIFC.dll")
# clr.AddReference("RevitAPIIFC")


# from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB.IFC import IFCExportOptions
import revit_script_util
from revit_script_util import Output

doc = revit_script_util.GetScriptDocument()
Output("✅ IFC Export 시작!")

try:
    file_name = "GUARD_HOUSE_export.ifc"
    export_folder = r"D:\mQ\RBP_Export_IFC\Output"
    export_path = os.path.join(export_folder, file_name)

    # 3D 뷰 가져오기
    collector = FilteredElementCollector(doc).OfClass(View)
    view3d = None
    for v in collector:
        if v.ViewType == ViewType.ThreeD and not v.IsTemplate:
            view3d = v
            break

    if view3d is None:
        raise Exception("❌ 3D 뷰를 찾을 수 없습니다.")

    options = IFCExportOptions()
    options.FilterViewId = view3d.Id
    options.FileVersion = "IFC2x3"
    options.ExportBaseQuantities = True

    doc.Export(export_folder, file_name, options)
    Output("✅ IFC Export 성공!")
    Output("📁 파일 경로: " + export_path)
    Output("🧭 3D 뷰 이름: " + view3d.Name)

except Exception as e:
    Output("❌ 오류 발생: " + str(e))
