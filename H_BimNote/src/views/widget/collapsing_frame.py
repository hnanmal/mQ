from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle


IMG_PATH = Path(__file__).parent.parent.parent.parent / "resource"
# IMG_PATH = Path(__file__).parent / "resource"
# IMG_PATH = "resource"


class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, _state, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self._state = _state

        # widget images
        self.images = [
            ttk.PhotoImage(file=IMG_PATH / "frame_close.png"),
            ttk.PhotoImage(file=IMG_PATH / "frame_open.png"),
        ]

    def add(self, child, title="", bootstyle=PRIMARY, collapsed=False, **kwargs):
        """Add a child to the collapsible frame

        Parameters:
            child (Frame): The child frame to add to the widget.
            title (str): The title appearing on the collapsible section header.
            bootstyle (str): The style to apply to the collapsible section header.
            collapsed (bool): Whether the group should start collapsed.
            **kwargs (Dict): Other optional keyword arguments.
        """
        self.kwargs = kwargs
        if child.winfo_class() != "TFrame":
            return

        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)
        self.frm = frm

        # header title
        header = ttk.Label(master=frm, text=title, bootstyle=(style_color, INVERSE))
        if kwargs.get("fontsize"):
            header.config(
                font=(
                    "Bahnschrift Light SemiCondensed",
                    kwargs.get("fontsize"),
                    "normal",
                )
            )
        else:
            header.config(font=("Bahnschrift Light SemiCondensed", 12, "normal"))
        if kwargs.get("textvariable"):
            header.configure(textvariable=kwargs.get("textvariable"))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child):
            self._state.toggle_height(self._state)
            return self._toggle_open_close(c)

        btn = ttk.Button(
            master=frm, image=self.images[0], bootstyle=style_color, command=_func
        )
        btn.pack(side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # Start collapsed if specified
        if collapsed:
            child.grid_remove()
            btn.configure(image=self.images[1])
            if kwargs.get("suggest_area") and hasattr(
                self._state, "project_WM_perRVT_SheetView"
            ):
                self._state.project_WM_perRVT_SheetView.renew_sheet_height()
                pass
        else:
            if kwargs.get("suggest_area") and hasattr(
                self._state, "project_WM_perRVT_SheetView"
            ):
                self._state.project_WM_perRVT_SheetView.rollback_sheet_height()
                pass

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button
        image accordingly.

        Parameters:

            child (Frame):
                The child element to add or remove from grid manager.
        """
        kwargs = self.kwargs
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
            if kwargs.get("suggest_area") and hasattr(
                self._state, "project_WM_perRVT_SheetView"
            ):
                self._state.project_WM_perRVT_SheetView.renew_sheet_height()
                pass
        else:
            child.grid()
            child.btn.configure(image=self.images[0])
            if kwargs.get("suggest_area") and hasattr(
                self._state, "project_WM_perRVT_SheetView"
            ):
                self._state.project_WM_perRVT_SheetView.rollback_sheet_height()


if __name__ == "__main__":

    app = ttk.Window(minsize=(300, 1))

    cf = CollapsingFrame(app)
    cf.pack(fill=BOTH)

    # option group 1
    group1 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group1, text=f"Option {x + 1}").pack(fill=X)
    cf.add(child=group1, title="Option Group 1", collapsed=True)

    # option group 2
    group2 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group2, text=f"Option {x + 1}").pack(fill=X)
    cf.add(group2, title="Option Group 2", bootstyle=DANGER)

    # option group 3
    group3 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group3, text=f"Option {x + 1}").pack(fill=X)
    cf.add(group3, title="Option Group 3", bootstyle=SUCCESS)

    app.mainloop()
