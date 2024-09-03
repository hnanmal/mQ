# # tests/test_core.py

# import unittest
# from src.core.state_management import AppState

# class TestAppState(unittest.TestCase):
#     def test_set_current_tab(self):
#         state = AppState()
#         state.set_current_tab("test_tab")
#         self.assertEqual(state.current_tab, "test_tab")

#     # Add more tests as needed

# if __name__ == "__main__":
#     unittest.main()

import tkinter

win = tkinter.Tk()


def func1(event):
    print("func1 - leftMouseClick")


def func2(event):
    print("func2 - rightMouseClick")


label = tkinter.Label(win, text="click this")
label.pack()
label.bind("<Button-1>", func1)
label.bind("<Button-2>", func2)

win.mainloop()
