# modules/ui.py

from modules.tabs.wm_group_tab import create_wm_matching_by_group_tab
from modules.tabs.single_area_tab import create_single_area_tab
from modules.tabs.three_area_tab import create_three_area_tab


class UIManager:
    def __init__(self, app):
        self.app = app

    def setup_ui(self):
        tab_names = [
            "패밀리 표준 구성도",
            "WM 그룹별 매칭",
            "계산 기준",
            "Room",
            "Floors",
            "Roofs",
            "Walls_Ext",
            "Walls_Int",
            "St_Fdn",
            "St_Col",
            "St_Framing",
            "Ceilings",
            "Doors",
            "Windows",
            "Stairs",
            "Railings",
            "Generic",
            "Manual_Input",
        ]

        self.app.top_level_items = tab_names[
            3:
        ]  # Assign top-level items to the app instance

        for name in tab_names:
            if name == "패밀리 표준 구성도":
                create_single_area_tab(self.app, name)
            elif name == "WM 그룹별 매칭":
                create_wm_matching_by_group_tab(self.app)
            else:
                create_three_area_tab(self.app, name)
