# Version: 1.0.14


class SearchManager:
    def __init__(self, app):
        self.app = app
        self.search_results = []
        self.search_index = 0
        self.last_search_term = ""

    def setup_search(self, button_frame):
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(button_frame, textvariable=self.search_var, width=30)
        search_entry.bind("<Return>", self.on_enter_key)
        search_button = ttk.Button(
            button_frame, text="Search", command=self.search_items
        )
        search_entry.pack(side="right", padx=2, pady=5)
        search_button.pack(side="right", padx=2, pady=5)

    def search_items(self):
        search_term = self.search_var.get().lower()
        if not search_term:
            return

        items = self.app.tree.get_children("")
        self.search_results = []

        def recursive_search(item):
            if search_term in self.app.tree.item(item, "values")[0].lower():
                self.search_results.append(item)
            for child in self.app.tree.get_children(item):
                recursive_search(child)

        for item in items:
            recursive_search(item)

        if self.search_results:
            self.search_index = 0
            self.select_search_result()

    def select_search_result(self):
        if self.search_results:
            item = self.search_results[self.search_index]
            self.app.tree.selection_set(item)
            self.app.tree.see(item)
            self.search_index = (self.search_index + 1) % len(self.search_results)

    def on_enter_key(self, event):
        search_term = self.search_var.get().lower()
        if search_term != self.last_search_term:
            self.search_results = []
            self.search_index = 0
            self.last_search_term = search_term

        if not self.search_results:
            self.search_items()
        else:
            self.select_search_result()
