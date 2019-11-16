# Write your code here :-)
import board
import pulseio
import time
import adafruit_irremote
import random
import math
import board
from i2cslave import I2CSlave

red = pulseio.PWMOut(board.D5, frequency=38000, duty_cycle=0)
green = pulseio.PWMOut(board.D6, frequency=38000, duty_cycle=0)
blue = pulseio.PWMOut(board.D7, frequency=38000, duty_cycle=0)

# No IR Out without an extra capacitor on the power supply
# irtx = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
# irout = pulseio.PulseOut(irtx)

# Measuring IR pulses
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)

# encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
#                                             zero=[550, 1700], trail=0)
decoder = adafruit_irremote.GenericDecode()


# i2c.writeto(0x42, bytes([0x42]), stop=False)
i2c_slave = I2CSlave(board.SCL, board.SDA, (0x42, 0x44))


def rgbOff():
    red.duty_cycle = 0xffff
    green.duty_cycle = 0xffff
    blue.duty_cycle = 0xffff

# https://codegolf.stackexchange.com/questions/150250/hsl-to-rgb-values
# input h=[0,6[ s=[0,1] L=[0,1]
def hsl2rgb(h,s,l):
    c=(1-abs(2*l-1))*s;
    m=l-c/2;
    x=c*(1-abs(h%2-1))+m;
    c+=m;
    return[c,m,x,c,m,x,m,c,x,m][7-int(h)*5%9:][:3]

def setColorHSL(h, s, l):
    rgb = hsl2rgb(h, s, l)

    #print(h, s, l, rgb)

    red.duty_cycle = math.floor((2**16-1) * (1-rgb[0]))
    green.duty_cycle = math.floor((2**16-1) * (1-rgb[1]))
    blue.duty_cycle = math.floor((2**16-1) * (1-rgb[2]))



def matchNerfPulses(pulses):
    if len(pulses) != 17:
        print("wrong number of pulses {}".format(len(pulses)))
        return None

    reference1 = [2957, 5996, 2974, 2009, 991, 1987, 987, 2008, 992, 1987, 983, 2008, 1962, 2012, 987, 2008, 966]
    reference2 = [2935, 6037, 2957, 2038, 940, 2047, 961, 2039, 914, 2073, 1957, 2042, 910, 2094, 940, 2042, 936]
    

    def matchAgainstKnownPulse(pulses, knownReference):
        for i in range(0, 17, 1):
            if math.fabs(pulses[i] - knownReference[i]) > 150:
                print("pulse {} does not match {} vs {}".format(i, pulses[i], knownReference[i]))
                return None
        return True

    if matchAgainstKnownPulse(pulses, reference1):
        print("Nerf Blast Team1")
        return 1
    if matchAgainstKnownPulse(pulses, reference2):
        print("Nerf Blast Team2")
        return 2
    return None


def doTheColorRampDance(hue, duration, upAndDown = False, count = 1):
    if upAndDown:
        duration = duration / 2

    while count > 0:
        for i in range(0, 100, 1):
            # we only go up to 50% lightness because it's white afterwards.
            setColorHSL(hue, 1, i/2/100)
            time.sleep(duration / 100)

        if upAndDown:
            for i in range(100, 0, -1):
                # we only go up to 50% lightness because it's white afterwards.
                setColorHSL(hue, 1, i/2/100)
                time.sleep(duration / 100)

        count = count - 1

rgbOff()
# [0, 6[
currentHue = 0
# 0 to 100
currentIntensity = 0
speed = 1

power = True

while True:
    if power:
        currentIntensity = currentIntensity + speed

        if currentIntensity >= 100:
            speed = speed * -1

        if currentIntensity <= 0:
            speed = speed * -1
            currentHue = (currentHue + 0.3) % 6

        setColorHSL(currentHue, 1, currentIntensity / 200)
    else:
        rgbOff()



    pulses = decoder.read_pulses(pulsein, blocking= False)
    if pulses:
        print("Heard", len(pulses), "Pulses:", pulses)

        nerfBlast = matchNerfPulses(pulses)
        if nerfBlast == 1:
            setColorHSL(1, 1, 0.5)
            time.sleep(2)
        elif nerfBlast == 2:
            setColorHSL(3, 1, 0.5)
            time.sleep(2)

        else:
            # Not a nerf blast - maybe a IR command
            try:
                code = decoder.decode_bits(pulses)
                print("Decoded:", code)
                if len(code) == 5 and code[0:4] == [0xde, 0xad, 0xbe, 0xef]:
                    print("Got command: {}".format(code[4]))
                    doTheColorRampDance(code[4] * 6.0 / 255, 2, True, 5)
                
                if code == [124, 93]:
                    print("Power!")
                    power = not power
                
            except adafruit_irremote.IRNECRepeatException:  # unusual short code!
                print("NEC repeat!")
            except adafruit_irremote.IRDecodeException as e:     # failed to decode
                print("Failed to decode: ", e.args)

# def matchCode(code, reference):
#    if len(code) == len(reference) and code