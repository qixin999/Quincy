import board
import neopixel
import time
import analogio
from simpleio import map_range

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2)

analog_in1 = analogio.AnalogIn(board.A1)
analog_in2 = analogio.AnalogIn(board.A2)

smooth_val = analog_in1.value

def weightedSmooth(current, in_val, weight):
    current = weight * in_val + ((1 - weight) * current)
    return current


r = 0
g = 0
b = 255

color = (r, g, b)
pixels.fill(color)
bright = 0

while True:
    reading = analog_in1.value
    smooth_val = weightedSmooth(smooth_val, reading, 0.25)

    scaled_val = map_range(smooth_val, 0, 65535, 0, 1)
    scaled_val = float(scaled_val)
    bright = scaled_val

    color = (int(bright * r), int(bright * g), int(bright * b))
    pixels.fill(color)

    reading2 = analog_in2.value
    print(reading2)

    if reading2 > 60000:
        r = 255
        g = 0
        b = 0

    else:
        r = 0
        g = 0
        b = 255

    time.sleep(0.01)


