# tests/test_models.py

import unittest
from src.models.wm_group import WMGroupManager

class TestWMGroupManager(unittest.TestCase):
    def test_load_wm_group_data(self):
        manager = WMGroupManager("path/to/test_wm_group_match.json")
        data = manager.get_wm_group_data()
        self.assertIn("item1", data)

    # Add more tests as needed

if __name__ == "__main__":
    unittest.main()
