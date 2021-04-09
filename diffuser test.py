# pwm code to drive a piezoelectric humidifier

# import modules
import time
import board
import pwmio
import analogio

# change this variable to change the frequency
MY_FREQ = 115000

# make a pwm object with pwmio.PWMOut on pin board.A1
pwm = pwmio.PWMOut(board.A1, frequency=MY_FREQ, duty_cycle=0)
photo = analogio.AnalogIn(board.A4)

# spray on is a 30% duty cycle
SPRAY_ON = int(0.4 * 65535)
# spray off must be 100% duty cycle!!! 0% shorts the inductors!
SPRAY_OFF = 65535

pwm.duty_cycle = SPRAY_ON

pulse_time = time.monotonic()
pulse_inc = (photo.value - 20000) / 45535

run_spray = True

# loop forever
while True:
    if time.monotonic() >= pulse_time:
        if run_spray:
            pulse_time = time.monotonic() + pulse_inc
        else:
            pulse_time = time.monotonic() + 0.5
        pulse_inc = (photo.value - 20000) / 45535
        print(pulse_time)
        run_spray = not run_spray
    # time.sleep(0.1)
    if run_spray:
        pwm.duty_cycle = SPRAY_ON
    else:
        pwm.duty_cycle = SPRAY_OFF

# 在这里写上你的代码 :-)
