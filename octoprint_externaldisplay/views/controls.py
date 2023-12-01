from PIL import Image, ImageDraw
from collections import namedtuple
from octoprint_externaldisplay.fonts import get_font
from octoprint_externaldisplay.canvas import Canvas


class ControlsView:
    COLOR_DEFAULT = "white"
    COLOR_DISABLED = "gray"
    COLOR_DANGER = "red"

    Action = namedtuple("Action", ["color", "label"])

    def __init__(self, canvas: Canvas, action_bar_size: int = 16):
        self.canvas = canvas
        self.action_bar_size = action_bar_size

        image_size = (canvas.image.height, action_bar_size)
        self._image = Image.new("RGB", image_size, "black")
        self._draw = ImageDraw.Draw(self._image)

    def draw(self, actions: list[Action]):
        self.clear()
        self.draw_actions(actions)

        rotated = self._image.transpose(Image.ROTATE_90)
        self.canvas.image.paste(rotated, (self.canvas.image.width - rotated.width, 0))

    def clear(self):
        self._draw.rectangle(((0, 0), self._image.size), fill="black")

    def draw_actions(self, actions: list[Action]):
        action_width = self._image.width // len(actions)

        self._draw.line(
            ((0, self.canvas.scale // 2), (self._image.width, self.canvas.scale // 2)),
            fill="white", width=self.canvas.scale)

        for i, action in enumerate(reversed(actions)):
            self.draw_action(action, action_width, i)

    def draw_action(self, action: Action, width: int, index: int):
        font = get_font("iosevka_regular", 10 * self.canvas.scale)

        x = width * index

        if index > 0:
            self._draw.line(((x, 0), (x, self._image.height)), fill="white", width=self.canvas.scale)

        self._draw.text((x + width // 2, self._image.height), action.label, fill=action.color, font=font, anchor="mb")
