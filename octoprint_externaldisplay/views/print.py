from collections import namedtuple
from octoprint_externaldisplay.fonts import get_font
from octoprint_externaldisplay.canvas import Canvas

Temperature = namedtuple("Temperature", ["current", "target"])

PrintViewData = namedtuple("FrameData", [
    "bed",
    "extruder",
    "progress",
    "time_elapsed",
    "time_remaining",
])


class PrintView:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw(self, data: PrintViewData):
        self.clear()
        self.draw_temperatures(data)
        self.draw_progress(data)
        self.draw_time(data)

    def clear(self):
        self.canvas.draw.rectangle(((0, 0), self.canvas.image.size), fill="black")

    def draw_temperatures(self, data: PrintViewData):
        offset = 4 * self.canvas.scale

        if data.bed is not None:
            self.draw_temperature(data.bed, (offset, self.canvas.image.height - offset), "ld")
        if data.extruder is not None:
            self.draw_temperature(data.extruder, (self.canvas.image.width - offset, self.canvas.image.height - offset),
                                  "rd")

    def draw_temperature(self, temperature: Temperature, position: tuple[int, int], anchor: str):
        text = f"{temperature.current:.0f}°C"
        font = get_font("iosevka_bold", 16 * self.canvas.scale)

        if temperature.target == 0:
            color = "gray"
        elif temperature.target - temperature.current > 1:
            color = "red"
        elif temperature.target - temperature.current < -1:
            color = "blue"
        else:
            color = "white"

        self.canvas.draw.text(position, text, fill=color, font=font, anchor=anchor)

    def draw_progress(self, data: PrintViewData):
        bottom_offset = 16 * self.canvas.scale
        diameter = self.canvas.image.width - 32 * self.canvas.scale
        line_width = 8 * self.canvas.scale

        x = (self.canvas.image.width - diameter) / 2
        y = (self.canvas.image.height - diameter - bottom_offset) / 2
        bounding_box = [(x, y), (x + diameter, y + diameter)]

        self.canvas.draw.arc(bounding_box, 0, 360, fill="gray", width=line_width)

        if data.progress:
            angle = data.progress / 100 * 360
            self.canvas.draw.arc(bounding_box, 0, angle, fill="white", width=line_width)

    def draw_time(self, data: PrintViewData):
        bottom_offset = 16 * self.canvas.scale
        position = (self.canvas.image.width / 2, (self.canvas.image.height - bottom_offset) / 2)
        font = get_font("iosevka_regular", 24 * self.canvas.scale)

        if data.time_remaining:
            text = self.format_time(data.time_remaining)
            self.canvas.draw.text(position, text, fill="white", font=font, anchor="mm")
        elif data.time_elapsed:
            text = self.format_time(data.time_elapsed)
            self.canvas.draw.text(position, text, fill="gray", font=font, anchor="mm")

    def format_time(self, seconds: int):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
