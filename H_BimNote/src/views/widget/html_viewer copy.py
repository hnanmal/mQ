from cefpython3 import cefpython as cef
import tkinter as tk
from tkinter import ttk
import os


class BrowserWidget(ttk.Frame):
    def __init__(self, parent, html_file=None, url=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Determine whether to load a local file or a URL
        if html_file:
            # Preprocess the path to handle backslashes
            path = os.path.abspath(html_file).replace("\\", "/")
            self.url = f"file:///{path}"
        elif url:
            self.url = url
        else:
            raise ValueError("Either 'html_file' or 'url' must be provided.")

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
        settings = {
            "multi_threaded_message_loop": False,
            "command_line_args_disabled": False,
        }

        switches = {
            "disable-gpu": "",
            "disable-gpu-compositing": "",
        }

        cef.Initialize(settings=settings, switches=switches)

    def create_browser(self):
        """Create a browser instance embedded in the Tkinter Frame."""
        window_info = cef.WindowInfo()
        window_info.SetAsChild(self.browser_frame.winfo_id(), [0, 0, 1000, 800])
        return cef.CreateBrowserSync(window_info=window_info, url=self.url)

    def _cef_loop(self):
        """Integrate CEF event loop with Tkinter."""
        cef.MessageLoopWork()
        self.after(10, self._cef_loop)

    def on_close(self):
        """Shutdown CEF properly when the widget or app closes."""
        cef.Shutdown()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1024x768")
    root.title("In-App Browser Widget")

    # Load a local HTML file
    local_file = "example.html"  # Replace with your HTML file path
    browser = BrowserWidget(root, html_file=local_file)
    browser.pack(fill="both", expand=True, padx=10, pady=10)

    # Properly shut down CEF when closing the app
    def on_close():
        browser.on_close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
