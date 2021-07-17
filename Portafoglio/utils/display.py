import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
disp.begin()
disp.clear()
disp.display()
image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)

def display(txt):
    draw.rectangle((0, 0, disp.width, disp.height), outline = 0, fill = 0)
    padding = 2

    font = max_font_size(txt)

    draw.text((padding, padding), txt, font = font, fill = 255)
    time.sleep(0.2)
    disp.image(image)
    disp.display()
    time.sleep(1)

    # print()
    # disp.clear()
    # disp.display()

def display_lines(arr):
    draw.rectangle((0, 0, disp.width, disp.height), outline = 0, fill = 0)
    padding = 2
    font = ImageFont.load_default()

    top = 0
    for word in arr:
        draw.text((padding, padding + top), word, font = font, fill = 255)
        top += 8
    
    time.sleep(0.2)
    disp.image(image)
    disp.display()
    time.sleep(3)

def max_font_size(txt):
    fontsize = 1
    img_fraction = 0.50
    font = ImageFont.truetype("arial.ttf", fontsize)

    while font.getsize(txt)[0] < img_fraction*image.size[0]:
        fontsize += 1
        font = ImageFont.truetype("arial.ttf", fontsize)

    fontsize -= 1
    font = ImageFont.truetype("arial.ttf", fontsize)
    return font