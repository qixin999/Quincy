# import modules
import time
import board
import pwmio
import analogio
import neopixel
from digitalio import DigitalInOut, Direction

button = DigitalInOut(board.A6)
button.direction = Direction.INPUT
buttonPre = True
buttonPressTime = 0
onoffMode = lightMode = 0

def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)

    return(r, g, b)

pixels = neopixel.NeoPixel(board.A5, 30)
photo = analogio.AnalogIn(board.A4)

color = (0, 0, 0)
pixels.fill(color)
i = float(photo.value)

MY_FREQ = 115000

# make 3 atomizer with pwmio.PWMOut on A1, A2 and A3
pwm1 = pwmio.PWMOut(board.A1, frequency=MY_FREQ, duty_cycle=0)
pwm2 = pwmio.PWMOut(board.A2, frequency=MY_FREQ, duty_cycle=0)
pwm3 = pwmio.PWMOut(board.A3, frequency=MY_FREQ, duty_cycle=0)

# spray on is a 30% duty cycle
SPRAY_ON = int(0.3 * 65535)
# spray off must be 100% duty cycle
SPRAY_OFF = 65535

pwm1.duty_cycle = SPRAY_ON
pwm2.duty_cycle = SPRAY_ON
pwm3.duty_cycle = SPRAY_ON

pulse_time1 = time.monotonic()
pulse_time2 = time.monotonic()
pulse_time3 = time.monotonic()

run_spray1 = True
run_spray2 = True
run_spray3 = True
timing = time.monotonic()
colorindex = 0

# loop forever
while True:
    # determine if button is pressed
    if button.value != buttonPre:
        buttonPre = button.value
        if not button.value:
            buttonPressTime = time.monotonic()
        else:
            # long press toggle the on or off
            if time.monotonic() >= buttonPressTime + 1:
                onoffMode += 1
            # short press toggle work mode or natural mode
            else:
                lightMode += 1

    if onoffMode > 1:
        onoffMode = 0
    if lightMode > 1:
        lightMode = 0

    # diffuser is on
    if onoffMode == 1:
        # natural mode
        if lightMode == 1:
            #translate the photo value to RGB value
            i = int(0.92 * i + 0.08 * photo.value / 65535 * 128)
            color = wheel(i)
            pixels.fill(color)

            # atomizer1 sparys follow the R value
            pulse_inc1 = wheel(i)[0] / 255 * 3
            # 3s is a spray on/off cycle
            a = 3 - pulse_inc1
            # atomizer2 sparys follow the G value
            pulse_inc2 = wheel(i)[1] / 255 * 3
            b = 3 - pulse_inc2
            # atomizer3 sparys follow the B value
            pulse_inc3 = wheel(i)[2] / 255 * 3
            c = 3 - pulse_inc3

            if time.monotonic() >= pulse_time1:
                if run_spray1:
                    pulse_time1 = time.monotonic() + pulse_inc1
                else:
                    pulse_time1 = time.monotonic() + a

                run_spray1 = not run_spray1

            if time.monotonic() >= pulse_time2:
                if run_spray2:
                    pulse_time2 = time.monotonic() + pulse_inc2
                else:
                    pulse_time2 = time.monotonic() + b

                run_spray2 = not run_spray2

            if time.monotonic() >= pulse_time3:
                if run_spray3:
                    pulse_time3 = time.monotonic() + pulse_inc3
                else:
                    pulse_time3 = time.monotonic() + c

                run_spray3 = not run_spray3

            # use pwn.duty_cycle to drive spray on/off
            if run_spray1:
                pwm1.duty_cycle = SPRAY_ON
            else:
                pwm1.duty_cycle = SPRAY_OFF

            if run_spray2:
                pwm2.duty_cycle = SPRAY_ON
            else:
                pwm2.duty_cycle = SPRAY_OFF

            if run_spray3:
                pwm3.duty_cycle = SPRAY_ON
            else:
                pwm3.duty_cycle = SPRAY_OFF
            time.sleep(0.02)

        # work mode
        else:
            # work for 50 min ( 5s here)
            if colorindex == 0:
                pixels.fill((0, 0, 255))
                pwm1.duty_cycle = SPRAY_ON
                pwm2.duty_cycle = SPRAY_OFF
                pwm3.duty_cycle = SPRAY_OFF
            # break for 10 min ( 1s here)
            else:
                pixels.fill((0, 255, 0))
                pwm2.duty_cycle = SPRAY_ON
                pwm1.duty_cycle = SPRAY_OFF
                pwm3.duty_cycle = SPRAY_OFF
            if time.monotonic() - timing >= 1:
                if colorindex:
                    timing = time.monotonic()
                    colorindex = 0
            if time.monotonic() - timing >= 5:
                if not colorindex:
                    timing = time.monotonic()
                    colorindex = 1

    # turn off the diffuser
    else:
        pwm1.duty_cycle = SPRAY_OFF
        pwm2.duty_cycle = SPRAY_OFF
        pwm3.duty_cycle = SPRAY_OFF
        pixels.fill((0, 0, 0))

    time.sleep(0.01)
