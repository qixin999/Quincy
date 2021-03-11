import board
import neopixel
import time
import analogio
import busio
import adafruit_am2320
from simpleio import map_range
from digitalio import DigitalInOut, Direction, Pull

analog_in1 = analogio.AnalogIn(board.A1)

i2c = busio.I2C(board.SCL, board.SDA)
am = adafruit_am2320.AM2320(i2c)
r = 255
b = 0

smooth_val = am.relative_humidity

def weightedSmooth(in_val, weight):
    global smooth_val
    smooth_val = weight * in_val + ((1 - weight) * smooth_val)
    return smooth_val

switch = DigitalInOut(board.SLIDE_SWITCH)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

button = DigitalInOut(board.A2)
button.direction = Direction.INPUT
buttonPre = True
buttonPressTime = 0
onoffMode = lightMode = 0
breath = 0
i = 1

analog_in3 = analogio.AnalogIn(board.A3)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10,)

modeColor = (50, 50, 50)
CLEAR = (0, 0, 0)

m = time.monotonic()
k = 0
while True:
    if time.monotonic() - m >= 0.3:
        m = time.monotonic()
        reading = am.relative_humidity
        smooth_val = weightedSmooth(reading, 0.3)
        scale_val = map_range(smooth_val, 35, 50, 0, 255)
        r = 255 - int(scale_val)
        b = int(scale_val)
        color = (r, 0, b)
        print(r, 0, b)
        time.sleep(0.01)
    if button.value != buttonPre:
        buttonPre = button.value
        if not button.value:
            buttonPressTime = time.monotonic()
        else:
            if time.monotonic() >= buttonPressTime + 1:
                onoffMode += 1
            else:
                lightMode += 1

    if onoffMode > 1:
        onoffMode = 0
    if lightMode > 1:
        lightMode = 0
    reading2 = analog_in3.value
    if onoffMode == 1:
        if reading2 > 30000:
            pixels[5] = CLEAR
        else:
            pixels[5] = ((100, 0, 0))

        if switch.value:
            pixels[3] = modeColor
            pixels[6] = CLEAR
            if lightMode == 1:
                pixels[4] = (0, 255, 0)
                reading1 = analog_in1.value
                if pixels[5] == CLEAR:
                    if reading1 < 10000:
                        pixels[2] = (r, 0, b)
                        pixels[1] = pixels[0] = pixels[9] = pixels[8] = \
                            pixels[7] = CLEAR
                    elif reading1 < 20000:
                        pixels[2] = pixels[1] = (r, 0, b)
                        pixels[0] = pixels[9] = pixels[8] = pixels[7] = CLEAR
                    elif reading1 < 30000:
                        pixels[2] = pixels[1] = pixels[0] = (r, 0, b)
                        pixels[9] = pixels[8] = pixels[7] = CLEAR
                    elif reading1 < 40000:
                        pixels[2] = pixels[1] = pixels[0] = \
                            pixels[9] = (r, 0, b)
                        pixels[8] = pixels[7] = CLEAR
                    elif reading1 < 50000:
                        pixels[2] = pixels[1] = pixels[0] = pixels[9] = \
                            pixels[8] = (r, 0, b)
                        pixels[7] = CLEAR
                    else:
                        pixels[2] = pixels[1] = pixels[0] = pixels[9] = \
                            pixels[8] = pixels[7] = (r, 0, b)
                else:
                    pixels[2] = pixels[1] = pixels[0] = pixels[9] = \
                            pixels[8] = pixels[7] = (0, 0, 0)
            else:
                pixels[4] = (0, breath, 0)
                pixels[2] = pixels[1] = pixels[0] = pixels[9] = \
                    pixels[8] = pixels[7] = (0, 0, 0)
                breath += i
                if breath > 50:
                    i = -i
                    time.sleep(0.01)
                if breath < 1:
                    i = -i
                    time.sleep(0.01)
        else:
            pixels[6] = modeColor
            pixels[3] = CLEAR
            pixels[4] = (0, 255, 0)
            print(reading)
            if pixels[5] == CLEAR:
                if reading > 40:
                    pixels[2] = pixels[1] = pixels[0] = pixels[9] = \
                        pixels[8] = pixels[7] = (0, 0, 0)
                else:
                    newList = [0, 0, 0, 0, 0, 0]
                    for j in range(6):
                        newList[j] = (0, 0, k - j * 10)
                    k += 5
                    if k == 255:
                        k = 0
                    for x in range(6):
                        pixels[(12 - x) % 10] = newList[x]
            else:
                pixels[2] = pixels[1] = pixels[0] = pixels[9] = \
                                pixels[8] = pixels[7] = (0, 0, 0)

    else:
        pixels.fill((0, 0, 0))

    time.sleep(0.01)
