from typing import Text
from RPLCD.i2c import CharLCD
import time

lcd = CharLCD('PCF8574', 0x27)

def display(txt):
    lcd.backlight_enabled = True
    lcd.clear()
    lcd.cursor_pos = (0, 3)
    lcd.create_char(1, (0b00000, 0b00000, 0b00000, 0b00111, 0b00100, 0b00100, 0b00100, 0b00100,))
    lcd.write_string('\x01')
    lcd.cursor_pos = (0, 4)
    lcd.write_string("------------")
    lcd.create_char(0, (0b00000, 0b00000, 0b00000, 0b11100, 0b00100, 0b00100, 0b00100, 0b00100))
    lcd.write_string("\x00")
    lcd.cursor_pos = (1, 3)
    lcd.write_string("|")
    lcd.cursor_pos = (1, 8)
    lcd.write_string(txt)
    lcd.cursor_pos = (1, 16)
    lcd.write_string("|")
    lcd.cursor_pos = (2, 3)
    lcd.write_string("|")
    lcd.cursor_pos = (2, 16)
    lcd.write_string("|")
    lcd.cursor_pos = (3, 3)
    lcd.create_char(2, (0b00100, 0b00100, 0b00100, 0b00111, 0b00000, 0b00000, 0b00000, 0b00000))
    lcd.write_string('\x02')
    lcd.cursor_pos = (3, 4)
    lcd.write_string("------------")
    lcd.create_char(3, (0b00100, 0b00100, 0b00100, 0b11100, 0b00000, 0b00000, 0b00000, 0b00000))
    lcd.write_string('\x03')
    time.sleep(5)
    lcd.backlight_enabled = False
    lcd.clear()

def display_lines(arr):
    lcd.clear()
    y = 0
    lcd.cursor_pos = (y,0)

    for word in arr:
        lcd.write_string(word)
        time.sleep(0.1)
        y += 1
        lcd.cursor_pos = (y,0)
        time.sleep(0.1)

    time.sleep(10)
    lcd.clear()

def display_string(txt):
    lcd.backlight_enabled = True
    lcd.clear()
    lcd.write_string(txt)
    lcd.backlight_enabled = False
