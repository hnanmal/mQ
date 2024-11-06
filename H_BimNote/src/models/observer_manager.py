class ObserverManager:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if callable(observer) and observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer added: {observer}")
        else:
            print("Error: Observer is not callable")

    def notify_observers(self, state):
        if not self._observers:
            print("Warning: No observers registered")
        for observer in self._observers:
            try:
                observer(state)
            except Exception as e:
                print(f"Error notifying observer {observer}: {e}")
