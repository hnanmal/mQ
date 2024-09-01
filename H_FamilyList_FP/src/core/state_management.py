# src/core/state_management.py

class AppState:
    def __init__(self):
        self._state = {}
        self.current_tab = None
        self.config = None
        self.wm_group_data = {}
        self.lock_status = {}

    def __getitem__(self, key):
        return self._state.get(key)

    def __setitem__(self, key, value):
        self._state[key] = value
        
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