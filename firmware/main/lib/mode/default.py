import time
from color import ShittyRgb
from ir.pulses import Pulses
from ir.codes import Codes
from ir import ShittyIr

def start():
    shit_ir = ShittyIr()
    shit_rgb = ShittyRgb()
    shit_rgb.on()
    # -- STATES --
    # [0, 6[
    current_hue = 0
    # 0 to 100
    current_intensity = 0
    speed = 1
    power = True
    # -- PULSE HANDLERS --
    def team_1():
        shit_rgb.set_color_hsl(1, 1, 0.5)
        time.sleep(2)
    def team_2():
        shit_rgb.set_color_hsl(3, 1, 0.5)
        time.sleep(2)
    pulse_handlers = {
        Pulses.nerf.NERF_TEAM_1: team_1,
        Pulses.nerf.NERF_TEAM_2: team_2,
    }
    # -- CODE HANDLERS --
    def match_me(code):
        print("Match Me!")
        shit_ir.blast([0xde, 0xad, 0xbe, 0xef, round(current_hue / 6 * 255)])
    def get_matched(code):
        print("Color Sync! Got command: {}".format(code[4]))
        shit_rgb.do_the_color_ramp_dance(code[4] * 6.0 / 255, 2, True, 5)
    def flip_power(code):
        print("Power!")
        power = not power
    code_handlers = {
        Codes.adafruit.ADAFRUIT_1: match_me,
        Codes.adafruit.ADAFRUIT_2: lambda code: shit_ir.tx.toggle(),
        Codes.shirtty.COLOR_SYNC: get_matched,
        Codes.sharp.POWER: flip_power
    }
    def handle(pulses):
        pulse_match = Pulses.match(pulses)
        if pulse_match:
            print("PULSE")
            pulse_handlers[pulse_match]()
            return
        code = shit_ir.rx.get_code(pulses)
        code_match = Codes.match(code, debug=True)
        if code_match:
            print("CODE")
            code_handlers[code_match](code)  
            return
    while True:
        if shit_rgb.is_on:
            if power:
                current_intensity = current_intensity + speed
                if current_intensity >= 100:
                    speed = speed * -1
                if current_intensity <= 0:
                    speed = speed * -1
                    current_hue = (current_hue + 0.3) % 6
                shit_rgb.set_color_hsl(current_hue, 1, current_intensity / 200)
            else:
                shit_rgb.rgb_off()
        pulses = shit_ir.rx.get_pulses()
        handle(pulses)