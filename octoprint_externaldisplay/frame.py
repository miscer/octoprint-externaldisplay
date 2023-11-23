from PIL import Image, ImageDraw, ImageFont

def generate_frame():
    # Create a black background image
    image = Image.new("RGB", (128, 128), "black")
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default(32)

    # Add the "Hello!" message to the image
    message = "Hello!"
    left, top, right, bottom = font.getbbox(message)
    text_width, text_height = right - left, bottom - top

    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2
    draw.text((x, y), message, font=font, fill="white")

    return image
