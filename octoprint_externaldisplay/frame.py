from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from pkg_resources import resource_stream

Temperature = namedtuple("Temperature", ["current", "target"])

FrameData = namedtuple("FrameData", [
    "bed",
    "extruder",
    "progress",
    "time_elapsed",
    "time_remaining",
])

iosevka_regular = ImageFont.truetype(resource_stream(__name__, "static/fonts/iosevka-regular.ttf"))

def generate_frame(data: FrameData):
    frame = Frame(data)
    frame.draw()

    return frame.image

class Frame:
    def __init__(self, size: tuple[int, int]):
        self.scale = 4
        self.size = size
        width, height = size

        self.image = Image.new("RGB", (width * self.scale, height * self.scale), "black")
        self.canvas = ImageDraw.Draw(self.image)
        self.canvas.font = iosevka_regular

    def draw(self, data: FrameData):
        self.clear()
        self.draw_temperatures(data)
        self.draw_progress(data)
        self.draw_time(data)

        return self.image.resize(self.size, Image.LANCZOS)

    def clear(self):
        self.canvas.rectangle([(0, 0), self.image.size], fill="black")

    def draw_temperatures(self, data: FrameData):
        offset = 4 * self.scale

        if data.bed is not None:
            self.draw_temperature(data.bed, (offset, self.image.height - offset), "ld")
        if data.extruder is not None:
            self.draw_temperature(data.extruder, (self.image.width - offset, self.image.height - offset), "rd")

    def draw_temperature(self, temperature: Temperature, position: tuple[int, int], anchor: str):
        text = f"{temperature.current:.0f}°C"
        font_size = 16 * self.scale

        if temperature.target == 0:
            color = "gray"
        elif temperature.target - temperature.current > 1:
            color = "red"
        elif temperature.target - temperature.current < -1:
            color = "blue"
        else:
            color = "white"

        self.canvas.text(position, text, fill=color, font_size=font_size, anchor=anchor)

    def draw_progress(self, data: FrameData):
        bottom_offset = 16 * self.scale
        diameter = self.image.width - 32 * self.scale
        line_width = 8 * self.scale

        x = (self.image.width - diameter) / 2
        y = (self.image.height - diameter - bottom_offset) / 2
        bounding_box = [(x, y), (x + diameter, y + diameter)]

        self.canvas.arc(bounding_box, 0, 360, fill="gray", width=line_width)
        
        if data.progress:
            angle = data.progress / 100 * 360
            self.canvas.arc(bounding_box, 0, angle, fill="white", width=line_width)
    
    def draw_time(self, data: FrameData):
        bottom_offset = 16 * self.scale
        position = (self.image.width / 2, (self.image.height - bottom_offset) / 2)
        font_size = 24 * self.scale

        if data.time_remaining:
            text = self.format_time(data.time_remaining)
            self.canvas.text(position, text, fill="white", font_size=font_size, anchor="mm")
        elif data.time_elapsed:
            text = self.format_time(data.time_elapsed)
            self.canvas.text(position, text, fill="gray", font_size=font_size, anchor="mm")
    
    def format_time(self, seconds: int):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}"
        else:
            return f"{minutes}:{seconds:02d}"