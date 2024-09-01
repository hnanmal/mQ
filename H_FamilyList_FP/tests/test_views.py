# tests/test_views.py

import unittest
from src.views.ui import create_main_window

class TestUI(unittest.TestCase):
    def test_create_main_window(self):
        state = None  # Use mock or test state
        root, notebook = create_main_window(state)
        self.assertIsNotNone(root)
        self.assertIsNotNone(notebook)

    # Add more tests as needed

if __name__ == "__main__":
    unittest.main()
