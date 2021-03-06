import board
import pulseio
import math
import time
# https://codegolf.stackexchange.com/questions/150250/hsl-to-rgb-values
# input h=[0,6[ s=[0,1] L=[0,1]
def hsl_to_rgb(h,s,l):
    c=(1-abs(2*l-1))*s
    m=l-c/2
    x=c*(1-abs(h%2-1))+m
    c+=m
    return[c,m,x,c,m,x,m,c,x,m][7-int(h)*5%9:][:3]

class ShittyRgb(object):
    def __init__(self):
        self.red = None
        self.green = None
        self.blue = None
        self.is_on = False
    def on(self):
        self.red = pulseio.PWMOut(board.D5, frequency=38000, duty_cycle=0)
        self.green = pulseio.PWMOut(board.D6, frequency=38000, duty_cycle=0)
        self.blue = pulseio.PWMOut(board.D7, frequency=38000, duty_cycle=0)
        self.rgb_off()
        self.is_on = True
    def off(self):
        self.red.deinit()
        self.green.deinit()
        self.blue.deinit()
        self.red = None
        self.green = None
        self.blue = None
        self.is_on = False
    def rgb_off(self):
        if self.is_on:
            self.red.duty_cycle = 0xffff
            self.green.duty_cycle = 0xffff
            self.blue.duty_cycle = 0xffff
    def set_color_hsl(self, h, s, l):
        if self.is_on:
            rgb = hsl_to_rgb(h, s, l)
            self.red.duty_cycle = math.floor((2**16-1) * (1-rgb[0]))
            self.green.duty_cycle = math.floor((2**16-1) * (1-rgb[1]))
            self.blue.duty_cycle = math.floor((2**16-1) * (1-rgb[2]))
    def do_the_color_ramp_dance(self, hue, duration, up_and_down = False, count = 1):
        if self.is_on:
            if up_and_down:
                duration = duration / 2
            while count > 0:
                for i in range(0, 100, 1):
                    # we only go up to 50% lightness because it's white afterwards.
                    self.set_color_hsl(hue, 1, i/2/100)
                    time.sleep(duration / 100)
                if up_and_down:
                    for i in range(100, 0, -1):
                        # we only go up to 50% lightness because it's white afterwards.
                        self.set_color_hsl(hue, 1, i/2/100)
                        time.sleep(duration / 100)
                count = count - 1
