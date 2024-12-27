from cefpython3 import cefpython as cef
import tkinter as tk
from tkinter import ttk
import os


class BrowserWidget(ttk.Frame):
    def __init__(self, parent, url, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.url = url

        # Initialize CEF
        self.init_cef()

        # Create a Frame to hold the browser
        self.browser_frame = ttk.Frame(self)
        self.browser_frame.pack(fill="both", expand=True)

        # Embed the browser
        self.browser = self.create_browser()

        # Start the CEF message loop
        self.after(10, self._cef_loop)

    def init_cef(self):
        """Initialize CEF with necessary configurations."""
        # Pass command-line arguments directly in settings
        settings = {
            "multi_threaded_message_loop": False,  # Required for Tkinter integration
            "command_line_args_disabled": False,  # Allow custom command-line arguments
        }

        switches = {
            "disable-gpu": "",  # Disable GPU rendering
            "disable-gpu-compositing": "",  # Prevent compositing issues
        }

        cef.Initialize(settings=settings, switches=switches)

    def create_browser(self):
        """Create a browser instance embedded in the Tkinter Frame."""
        window_info = cef.WindowInfo()
        # Embed the browser into the widget
        window_info.SetAsChild(self.browser_frame.winfo_id(), [0, 0, 800, 600])
        return cef.CreateBrowserSync(window_info=window_info, url=self.url)

    def _cef_loop(self):
        """Integrate CEF event loop with Tkinter."""
        cef.MessageLoopWork()
        self.after(10, self._cef_loop)

    def on_close(self):
        """Shutdown CEF properly when the widget or app closes."""
        cef.Shutdown()


# Example usage in a larger application
if __name__ == "__main__":
    # Initialize the main application window
    root = tk.Tk()
    root.geometry("1024x768")
    root.title("In-App Browser Widget")

    # Create the BrowserWidget
    browser = BrowserWidget(root, url="https://www.python.org")
    browser.pack(fill="both", expand=True, padx=10, pady=10)

    # Properly shut down CEF when closing the app
    def on_close():
        browser.on_close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
