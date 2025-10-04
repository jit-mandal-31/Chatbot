class ChatMemory:
    def __init__(self, window_size=3):
        self.window_size = window_size
        self.history = []

    def add(self, speaker, text):
        self.history.append(f"{speaker}: {text}")
        if len(self.history) > self.window_size * 2:
            self.history.pop(0)

    def get_context(self):
        return "\n".join(self.history)
class ChatMemory:
    def __init__(self, window_size=3):
        self.window_size = window_size
        self.history = []

    def add(self, speaker, text):
        self.history.append(f"{speaker}: {text}")
        if len(self.history) > self.window_size * 2:
            self.history.pop(0)

    def get_context(self):
        return "\n".join(self.history)
