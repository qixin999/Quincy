import board
import time
import touchio
import neopixel

touchPin1 = touchio.TouchIn(board.A1)
touchPin2 = touchio.TouchIn(board.A2)
touchPin3 = touchio.TouchIn(board.A3)
touchPin4 = touchio.TouchIn(board.A4)
touchPin5 = touchio.TouchIn(board.A5)
touchPin6 = touchio.TouchIn(board.A6)
touchPin7 = touchio.TouchIn(board.TX)

t1Pre = False

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)
r = g = b = 1
status = 0

while True:
    if touchPin1.value != t1Pre:
        t1Pre = touchPin1.value

        if touchPin1.value:
            status += 1

        if status > 1:
            status = 0

    if status == 0:
        pixels.fill((0, 0, 0))

    else:
        if touchPin2.value:
            r += 0.5
            if r > 255:
                r = 255

        if touchPin3.value:
            r -= 0.5
            if r < 0:
                r = 0

        if touchPin4.value:
            g += 0.5
            if g > 255:
                g = 255

        if touchPin5.value:
            g -= 0.5
            if g < 0:
                g = 0

        if touchPin6.value:
            b += 0.5
            if b > 255:
                b = 255

        if touchPin7.value:
            b -= 0.5
            if b < 0:
                b = 0
        pixels.fill((r, g, b))


    time.sleep(0.01)
