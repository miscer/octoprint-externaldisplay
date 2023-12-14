class Event:
    pass


class ButtonPressEvent(Event):
    def __init__(self, button):
        self.button = button


class OctoPrintEvent(Event):
    def __init__(self, name: str, payload: dict):
        self.name = name
        self.payload = payload
