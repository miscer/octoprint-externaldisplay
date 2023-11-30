from PIL import Image, ImageDraw


class Canvas:
    def __init__(self, size: tuple[int, int], scale: int = 4):
        self.size = size
        self.scale = scale

        width, height = size
        self.image = Image.new("RGB", (width * self.scale, height * self.scale), "black")

        self.draw = ImageDraw.Draw(self.image)

    def get_image(self):
        return self.image.resize(self.size, Image.LANCZOS)
