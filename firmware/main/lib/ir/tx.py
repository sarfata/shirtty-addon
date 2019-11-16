import adafruit_irremote
import pulseio
import board

class IrTx(object):
    def __init__(self):
        self.irout = None
        self.irtx = None     
        self.encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
                                                zero=[550, 1700], trail=0)

    def is_on(self):
        return self.irout is not None and self.irtx is not None

    def on(self):
        # No IR Out without an extra capacitor on the power supply
        self.irtx = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
        self.irout = pulseio.PulseOut(self.irtx)

    def off(self):
        self.irout.deinit()
        self.irtx.deinit()
        self.irout = None
        self.irtx = None

    def toggle(self):
        if self.is_on():
            print("Turn off")
            self.off()
        else:
            print("Turn on")
            self.on()

    def send_pulses(self, pulses):
        if self.is_on():
            self.encoder.transmit(self.irout, pulses)
