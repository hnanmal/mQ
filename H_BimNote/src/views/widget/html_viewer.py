from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import tkinter as tk
import os
import sys


class BrowserWidget(QWidget):
    def __init__(self, parent=None, html_file=None, url=None):
        super().__init__(parent)

        # Determine whether to load a local file or a URL
        if html_file:
            path = os.path.abspath(html_file).replace("\\", "/")
            self.url = f"file:///{path}"
        elif url:
            self.url = url
        else:
            raise ValueError("Either 'html_file' or 'url' must be provided.")

        # Set up layout for the browser
        layout = QVBoxLayout(self)

        # Create the web view
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        # Load the provided URL or HTML file
        self.browser.setUrl(self.url)


class EmbeddedBrowser:
    def __init__(self, parent, html_file=None, url=None):
        self.parent = parent

        # Create the PyQt5 application
        self.qt_app = QApplication.instance()
        if not self.qt_app:
            self.qt_app = QApplication([])

        # Create the BrowserWidget
        self.browser_widget = BrowserWidget(html_file=html_file, url=url)

        # Create a tkinter Frame to hold the browser
        self.tk_frame = tk.Frame(self.parent)
        self.tk_frame.pack(fill="both", expand=True)

        # Embed the PyQt5 widget into the tkinter Frame
        self.browser_widget.winId()  # Ensure the widget has a native handle
        self.embed_browser()

    def embed_browser(self):
        # Place the PyQt5 widget inside the tkinter Frame
        self.browser_widget.setParent(None)
        self.browser_widget.setGeometry(
            0, 0, self.tk_frame.winfo_width(), self.tk_frame.winfo_height()
        )

        # Handle resizing
        self.tk_frame.bind("<Configure>", self.resize_browser)

    def resize_browser(self, event):
        self.browser_widget.setGeometry(0, 0, event.width, event.height)

    # Example usage in a tkinter application


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1024x768")
    root.title("Embedded Browser in Tkinter")

    # Load a local HTML file
    html_file = "example.html"  # Replace with your HTML file path
    browser = EmbeddedBrowser(root, html_file=html_file)

    root.mainloop()
