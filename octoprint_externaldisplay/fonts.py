from pkg_resources import resource_stream
from PIL import ImageFont

font_streams = {
    'iosevka_regular': resource_stream(__name__, "static/fonts/iosevka-regular.ttf"),
    'iosevka_medium': resource_stream(__name__, "static/fonts/iosevka-medium.ttf"),
    'iosevka_bold': resource_stream(__name__, "static/fonts/iosevka-bold.ttf"),
}

pillow_fonts = {}

def get_font(font_name, font_size):
    key = (font_name, font_size)

    if key not in pillow_fonts:
        stream = font_streams[font_name]
        stream.seek(0)
        
        pillow_fonts[key] = ImageFont.truetype(stream, font_size)
    
    return pillow_fonts[key]
