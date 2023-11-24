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
    def __init__(self, data: FrameData):
        self.data = data
        self.image = Image.new("RGB", (128, 128), "black")
        self.canvas = ImageDraw.Draw(self.image)
        self.canvas.font = iosevka_regular

    def draw(self):
        self.draw_temperatures()
        self.draw_progress()
        self.draw_time()

    def draw_temperatures(self):
        if self.data.bed is not None:
            self.draw_temperature(self.data.bed, (4, self.image.height - 4), "ld")
        if self.data.extruder is not None:
            self.draw_temperature(self.data.extruder, (self.image.width - 4, self.image.height - 4), "rd")

    def draw_temperature(self, temperature: Temperature, position: tuple[int, int], anchor: str):
        text = f"{temperature.current:.0f}°C"

        if temperature.target == 0:
            color = "gray"
        elif temperature.target - temperature.current > 1:
            color = "red"
        elif temperature.target - temperature.current < -1:
            color = "blue"
        else:
            color = "white"

        self.canvas.text(position, text, fill=color, font_size=16, anchor=anchor)

    def draw_progress(self):
        bottom_offset = 16
        diameter = self.image.width - 32

        x = (self.image.width - diameter) / 2
        y = (self.image.height - diameter - bottom_offset) / 2
        bounding_box = [(x, y), (x + diameter, y + diameter)]

        self.canvas.arc(bounding_box, 0, 360, fill="gray", width=8)
        
        if self.data.progress:
            angle = self.data.progress / 100 * 360
            self.canvas.arc(bounding_box, 0, angle, fill="white", width=8)
    
    def draw_time(self):
        bottom_offset = 16

        if self.data.time_remaining:
            text = self.format_time(self.data.time_remaining)
            position = (self.image.width / 2, (self.image.height - bottom_offset) / 2)
            self.canvas.text(position, text, fill="white", font_size=24, anchor="mm")
    
    def format_time(self, seconds: int):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}"
        else:
            return f"{minutes}:{seconds:02d}"