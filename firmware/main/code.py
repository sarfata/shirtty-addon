# Write your code here :-)
import board
import pulseio
import time
import random
import math
import board
from i2cslave import I2CSlave
from color import rgb_off, set_color_hsl, do_the_color_ramp_dance, hsl_to_rgb
from ir.pulses import Pulses
from ir.codes import Codes
from ir import ShittyIr
from pixels import ShittyPixels

# i2c.writeto(0x42, bytes([0x42]), stop=False)
i2c_slave = I2CSlave(board.SCL, board.SDA, (0x42, 0x44))

rgb_off()
# [0, 6[
current_hue = 0
# 0 to 100
current_intensity = 0
speed = 1

power = True

shit_ir = ShittyIr()
shit_pixels = ShittyPixels()

pixels_start_hue = 0

def handle_pulses(pulses):
    pulse_match = Pulses.match(pulses)
    if pulse_match is not None:
        if pulse_match == Pulses.nerf.NERF_TEAM_1:
            set_color_hsl(1, 1, 0.5)
            time.sleep(2)
            return
        elif pulse_match == Pulses.nerf.NERF_TEAM_2:
            set_color_hsl(3, 1, 0.5)
            time.sleep(2)
            return
    # Not a nerf blast - maybe a IR command
    code = shit_ir.rx.get_code(pulses)
    code_match = Codes.match(code)
    if code_match is not None and pulse_match is None:
        if code_match == Codes.adafruit.ADAFRUIT_2:
            shit_ir.tx.toggle()
        elif code_match == Codes.adafruit.ADAFRUIT_1:
            print("Infect!")
            shit_ir.blast([0xde, 0xad, 0xbe, 0xef, round(current_hue / 6 * 255)])

        elif code_match == Codes.adafruit.ADAFRUIT_3:
            shit_pixels.toggle()
        elif code_match == Codes.shirtty.COLOR_SYNC:
            print("Color Sync! Got command: {}".format(code[4]))
            do_the_color_ramp_dance(code[4] * 6.0 / 255, 2, True, 5)
        elif code_match == Codes.sharp.POWER:
            print("Power!")
            power = not power
    return

while True:
    # builtin RGB
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

    # pixels
    if shit_pixels.is_on():
        for i in range(0, 64, 1):
            row = round(i / 8)
            column = i % 8
            hue = (pixels_start_hue + row / 3 + column / 5) % 6

            rgb = hsl_to_rgb(hue, 1, 0.02)
            shit_pixels.pixels[i] = (round(rgb[0]*255), round(rgb[1]*255), round(rgb[2]*255))

        shit_pixels.pixels.show()
        pixels_start_hue = pixels_start_hue + .3

    pulses = shit_ir.rx.get_pulses()
    handle_pulses(pulses)
