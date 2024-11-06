from src.models.observer_manager import ObserverManager


GWM_headers = [
    "분류",
    "G-WM",
    "ITEM",
    # "WM_code",
    # "Work Master",
    # "Spec",
    # "Unit",
]


class AppState:
    def __init__(self, logging_text_widget):
        self._state = {}  ## 필요 없으면 나중에 삭제
        self.observer_manager = ObserverManager()
        self.GWM_headers = GWM_headers

        self.current_tab = None
        self.previous_tab = None  # Track the previous tab
        self.config = None
        self.wm_group_data = {}
        self.lock_status = {}
        self.logging_text_widget = logging_text_widget
        self.clipboard_data = None  # 추가: 클립보드 데이터를 저장하는 필드
        # self.project_info = None  # Loaded project data
        self.project_info = {}
        self.undo_stack = []

    ################### 옵저버 관련 #################################
    # 상태 업데이트 함수
    def update_S_GWM_data(self, new_data):
        print("update_sheet_data_start")

        # self.project_info["GWM"] = new_data
        self.project_info.update({"S-GWM": new_data})
        self.observer_manager.notify_observers(self)

        print("update_sheet_data_end")

    # 상태 업데이트 함수
    def update_project_info(self, new_data):
        self.project_info.update(new_data)
        self.observer_manager.notify_observers(self)

    ################### 옵저버 관련 #################################

    def __getitem__(self, key):
        return self._state.get(key)

    def __setitem__(self, key, value):
        self._state[key] = value

    # Add getter and setter for clipboard_data
    def get_clipboard_data(self):
        return self.clipboard_data

    def get_current_tab(self):
        """Return the currently selected tab."""
        return self.current_tab

    def set_clipboard_data(self, data):
        self.clipboard_data = data

    def set_current_tab(self, tab_name):
        self.current_tab = tab_name

    def load_config(self, config_data):
        self.config = config_data

    def update_wm_group_data(self, data):
        self.wm_group_data = data

    def set_lock_status(self, item_name, status):
        self.lock_status[item_name] = status

    def get_lock_status(self, item_name):
        return self.lock_status.get(item_name, False)

    # Method to get and set previous tab
    def get_previous_tab(self):
        return self.previous_tab

    def set_previous_tab(self, tab_name):
        self.previous_tab = tab_name
