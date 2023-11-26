import mmap
import os


class Framebuffer:
    def __init__(self, path):
        self.width = 129
        self.height = 130
        self.bytes_per_pixel = 2

        self.path = path
        self.fb_file = os.open(path, os.O_RDWR)
        self.fb_mmap = mmap.mmap(self.fb_file, self.width * self.height * self.bytes_per_pixel, prot=mmap.PROT_WRITE)
    
    def close(self):
        self.fb_mmap.close()
        os.close(self.fb_file)

    def write(self, image):
        img_rgb565 = image.convert('BGR;16')

        self.fb_mmap.seek(0)
        self.fb_mmap.write(img_rgb565.tobytes())
        self.fb_mmap.flush()