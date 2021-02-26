import board
import neopixel
import time
import analogio
from simpleio import map_range

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2)

analog_in1 = analogio.AnalogIn(board.A1)
analog_in2 = analogio.AnalogIn(board.A2)

smooth_val = analog_in2.value
def weightedSmooth(in_val, weight):
    global smooth_val
    smooth_val = weight * in_val + ((1 - weight) * smooth_val)
    return smooth_val

r = 255
g = 0
b = 0
color = (r, g, b)

bright = 0

while True:
    reading = analog_in1.value
    bright = map_range(reading, 0, 65535, 0, 1)
    bright = float(bright)
    print(bright)
    color = (int(bright * r), int(bright * g), int(bright * b))

    reading2 = analog_in2.value
    smooth_val = weightedSmooth(reading2, 0.02)

    scale_val = map_range(smooth_val, 30000, 61000, 0, 255)
    print(scale_val)
    r = 255 - int(scale_val)
    b = int(scale_val)
    pixels.fill(color)

    time.sleep(0.01)


