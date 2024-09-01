# tests/test_core.py

import unittest
from src.core.state_management import AppState

class TestAppState(unittest.TestCase):
    def test_set_current_tab(self):
        state = AppState()
        state.set_current_tab("test_tab")
        self.assertEqual(state.current_tab, "test_tab")

    # Add more tests as needed

if __name__ == "__main__":
    unittest.main()
