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

irtx = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
irout = pulseio.PulseOut(irtx)

# Measuring IR pulses
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)

encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
                                            zero=[550, 1700], trail=0)
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

def matchNerfPulses(pulses):
    if len(pulses) != 17:
        print("wrong number of pulses {}".format(len(pulses)))
        return None

    reference = [2935, 6037, 2957, 2038, 940, 2047, 961, 2039, 914, 2073, 1957, 2042, 910, 2094, 940, 2042, 936]
    for i in range(0, 17, 1):
        if math.fabs(pulses[i] - reference[i]) > 150:
            print("pulse {} does not match {} vs {}".format(i, pulses[i], reference[i]))
            return None

    return True


while True:
    print("Looping!")

    rgbOff()

    # empty pulse buffer so we do not react to last message we sent
    pulses = decoder.read_pulses(pulsein, blocking= False)

    # Pick a random hue
    hue = random.random() * 6

    # sleep for random number of sec.
    sleepUntil = time.monotonic() + random.randint(3, 10)
    while time.monotonic() < sleepUntil:
        pulses = decoder.read_pulses(pulsein, blocking= False)
        if pulses:
            print("Heard", len(pulses), "Pulses:", pulses)

            if matchNerfPulses(pulses):
                print("We have been blasted!!")
                for hue in range(0, 6, 2):
                    doTheColorRampDance(hue, 0.5, True)
            else:
                print("not a nerf blast")


            try:
                code = decoder.decode_bits(pulses)
                print("Decoded:", code)
                if len(code) == 5 and code[0:4] == [0xde, 0xad, 0xbe, 0xef]:
                    print("Got command: {}".format(code[4]))
                    doTheColorRampDance(code[4] * 6.0 / 255, 2, True, 5)
            except adafruit_irremote.IRNECRepeatException:  # unusual short code!
                print("NEC repeat!")
            except adafruit_irremote.IRDecodeException as e:     # failed to decode
                print("Failed to decode: ", e.args)

        # Check for i2c command
        r = i2c_slave.request()
        if r:
            with r:  # Closes the transfer if necessary by sending a NACK or feeding the master dummy bytes
                print("got i2c request! addr={} ".format(repr(r)))
                if r.address == 0x42:
                    if not r.is_read:  # Master write which is Slave read
                        b = r.read(1)

                        print("read bytes: {}".format(b))
                        if (len(b) == 1):
                            doTheColorRampDance(b[0] * 6.0 / 255, 2, True, 1)




    doTheColorRampDance(hue, 4, False)

    encoder.transmit(irout, [0xde, 0xad, 0xbe, 0xef, round(hue / 6 * 255)])
    doTheColorRampDance(hue, 2, True, 5)


