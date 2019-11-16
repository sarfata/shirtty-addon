# Write your code here :-)
import board
import pulseio
import time
import random
import math
import board
from i2cslave import I2CSlave
from lib.color import rgb_off, set_color_hsl, do_the_color_ramp_dance
from lib.ir.get import get_pulses, get_code
from lib.ir.pulses import Pulses
from lib.ir.codes import Codes

# i2c.writeto(0x42, bytes([0x42]), stop=False)
i2c_slave = I2CSlave(board.SCL, board.SDA, (0x42, 0x44))

# Measuring IR pulses
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)

rgb_off()
# [0, 6[
current_hue = 0
# 0 to 100
current_intensity = 0
speed = 1

power = True

def handle_pulses(pulses):
    if pulses:
        pulse_match = Pulses.match(pulses)
        if pulse_match == Pulses.nerf.NERF_TEAM_1:
            set_color_hsl(1, 1, 0.5)
            time.sleep(2)
            return
        elif pulse_match == Pulses.nerf.NERF_TEAM_2:
            set_color_hsl(3, 1, 0.5)
            time.sleep(2)
            return

        # Not a nerf blast - maybe a IR command
        code = Codes.match(get_code(pulses))
        if code is not None:
            if code == Codes.adafruit.ADAFRUIT_1:
                print("One!")

            # TODO: fix
            elif len(code) == 5 and code[0:4] == [0xde, 0xad, 0xbe, 0xef]:
                print("Got command: {}".format(code[4]))
                do_the_color_ramp_dance(code[4] * 6.0 / 255, 2, True, 5)

            # TODO fix
            elif code == [124, 93]:
                print("Power!")
                power = not power

            # airbnb remote [223, 32, 239, 16]
        return

while True:
    if power:
        current_intensity = current_intensity + speed

        if current_intensity >= 100:
            speed = speed * -1

        if current_intensity <= 0:
            speed = speed * -1
            current_hue = (current_hue + 0.3) % 6

        set_color_hsl(current_hue, 1, current_intensity / 200)
    else:
        rgb_off()

    pulses = get_pulses(pulsein)
    handle_pulses(pulses)
