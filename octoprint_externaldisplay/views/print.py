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
    def __init__(self, canvas: Canvas, position: tuple[int, int], size: tuple[int, int]):
        self.canvas = canvas
        self.x, self.y = position
        self.width, self.height = size

    def draw(self, data: PrintViewData):
        self.clear()
        self.draw_temperatures(data)
        self.draw_progress(data)
        self.draw_time(data)

    def clear(self):
        self.canvas.draw.rectangle(((self.x, self.y), (self.x + self.width, self.y + self.height)), fill="black")

    def draw_temperatures(self, data: PrintViewData):
        offset = 4 * self.canvas.scale

        if data.bed is not None:
            position = (self.x + offset, self.y + self.height - offset)
            self.draw_temperature(data.bed, position, "ld")
        if data.extruder is not None:
            position = (self.x + self.width - offset, self.y + self.height - offset)
            self.draw_temperature(data.extruder, position, "rd")

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
        diameter = self.width - 32 * self.canvas.scale
        line_width = 8 * self.canvas.scale

        x = self.x + (self.width - diameter) / 2
        y = self.y + (self.height - diameter - bottom_offset) / 2
        bounding_box = [(x, y), (x + diameter, y + diameter)]

        self.canvas.draw.arc(bounding_box, 0, 360, fill="gray", width=line_width)

        if data.progress:
            angle = (270 + data.progress / 100 * 360) % 360
            self.canvas.draw.arc(bounding_box, 270, angle, fill="white", width=line_width)

    def draw_time(self, data: PrintViewData):
        bottom_offset = 16 * self.canvas.scale
        position = (self.x + (self.width / 2), self.y + (self.height - bottom_offset) / 2)
        font = get_font("iosevka_regular", 20 * self.canvas.scale)

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
