class Manager:
    def __init__(self):
        self.current = None
        self.controllers = {}

    def register(self, name, controller):
        self.controllers[name] = controller

    def navigate(self, name):
        if self.current and hasattr(self.current, 'leave'):
            self.current.leave()

        self.current = self.controllers[name]

        if hasattr(self.current, 'enter'):
            self.current.enter()
