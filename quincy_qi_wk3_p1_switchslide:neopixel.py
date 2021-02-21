import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull

switch = DigitalInOut(board.SLIDE_SWITCH)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.3)


color1 = (200, 15, 165)
color2 = (0, 0, 0)

while True:
    if switch.value:
        pixels.fill(color1)
    else:
        pixels.fill(color2)

    time.sleep(0.05)
