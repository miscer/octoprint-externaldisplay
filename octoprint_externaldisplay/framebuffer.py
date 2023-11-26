import mmap
import os
import fcntl
import ctypes

FBIOGET_VSCREENINFO = 0x4600
FBIOGET_FSCREENINFO = 0x4602

class FixScreenInfo(ctypes.Structure):
    _fields_ = [
        ('id_name', ctypes.c_char * 16),
        ('smem_start', ctypes.c_ulong),
        ('smem_len', ctypes.c_uint32),
        ('type', ctypes.c_uint32),
        ('type_aux', ctypes.c_uint32),
        ('visual', ctypes.c_uint32),
        ('xpanstep', ctypes.c_uint16),
        ('ypanstep', ctypes.c_uint16),
        ('ywrapstep', ctypes.c_uint16),
        ('line_length', ctypes.c_uint32),
        ('mmio_start', ctypes.c_ulong),
        ('mmio_len', ctypes.c_uint32),
        ('accel', ctypes.c_uint32),
        ('reserved', ctypes.c_uint16 * 3),
    ]


class FbBitField(ctypes.Structure):
    _fields_ = [
        ('offset', ctypes.c_uint32),
        ('length', ctypes.c_uint32),
        ('msb_right', ctypes.c_uint32),
    ]


class VarScreenInfo(ctypes.Structure):
    _fields_ = [
        ('xres', ctypes.c_uint32),
        ('yres', ctypes.c_uint32),
        ('xres_virtual', ctypes.c_uint32),
        ('yres_virtual', ctypes.c_uint32),
        ('xoffset', ctypes.c_uint32),
        ('yoffset', ctypes.c_uint32),

        ('bits_per_pixel', ctypes.c_uint32),
        ('grayscale', ctypes.c_uint32),

        ('red', FbBitField),
        ('green', FbBitField),
        ('blue', FbBitField),
        ('transp', FbBitField),
    ]


class FramebufferInfo:
    def __init__(self, framebuffer_path):
        self.framebuffer_path = framebuffer_path

    def ioctl(self, request, arg):
        with open(self.framebuffer_path, 'rb') as fb:
            return fcntl.ioctl(fb.fileno(), request, arg)

    def get_var_info(self):
        var_info = VarScreenInfo()
        self.ioctl(FBIOGET_VSCREENINFO, var_info)
        return var_info

    def get_fix_info(self):
        fix_info = FixScreenInfo()
        self.ioctl(FBIOGET_FSCREENINFO, fix_info)
        return fix_info


class Framebuffer:
    def __init__(self, path):
        self.path = path
        self.read_info()

        self.fb_file = os.open(path, os.O_RDWR)
        self.fb_mmap = mmap.mmap(self.fb_file, self.fix_info.smem_len, prot=mmap.PROT_WRITE)

    def read_info(self):
        info = FramebufferInfo(self.path)
        self.fix_info = info.get_fix_info()
        self.var_info = info.get_var_info()

    def get_size(self):
        return (self.var_info.xres, self.var_info.yres)

    def get_color_depth(self):
        return self.var_info.bits_per_pixel
    
    def close(self):
        self.fb_mmap.close()
        os.close(self.fb_file)

    def write(self, image):
        fb_image = image

        if self.var_info.bits_per_pixel == 16:
            fb_image = image.convert('BGR;16')

        self.fb_mmap.seek(0)
        self.fb_mmap.write(fb_image.tobytes())
        self.fb_mmap.flush()
