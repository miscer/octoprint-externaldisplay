class Event:
    pass


class ButtonPressEvent(Event):
    def __init__(self, button):
        self.button = button
