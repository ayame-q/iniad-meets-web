from PIL import ImageFont, ImageDraw, Image
from config import settings
import os

def add_text_to_image(img, text, font_size, top, left, max_length=740):
    font_path = os.path.join(settings.BASE_DIR, "meets/mplus-1c-light.ttf")
    font_color = (255, 255, 255)
    position = (left, top)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'

    draw.text(position, text, font_color, font=font)

    return img

def make_share_image(score, full):
    base_img = Image.open(os.path.join(settings.BASE_DIR, "meets/quiz_snsshare.png")).copy()
    base_img = add_text_to_image(base_img, str(full), 72, 703, 964)
    img = add_text_to_image(base_img, str(score), 180, 590, 1549)

    return img
