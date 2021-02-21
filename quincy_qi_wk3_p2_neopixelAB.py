import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull

a = DigitalInOut(board.BUTTON_A)
b = DigitalInOut(board.BUTTON_B)
a.direction = Direction.INPUT
b.direction = Direction.INPUT
a.pull = Pull.DOWN
b.pull = Pull.DOWN
aPre = False
bPre = False

switch = DigitalInOut(board.SLIDE_SWITCH)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.25)


WHITE = (255, 255, 255)
ORANGE = (255, 50, 0)
BLUE = (0, 0, 255)
CLEAR = (0, 0, 0)
color = WHITE

while True:
    if switch.value:

        if a.value != aPre:
            aPre = a.value

            if not aPre:
                color = ORANGE
        elif b.value != bPre:
            bPre = b.value

            if not bPre:
                color = BLUE

    else:
        pixels.fill(CLEAR)

    pixels.fill(color)
    time.sleep(0.01)
