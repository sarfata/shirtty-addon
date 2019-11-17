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
class IrRx(object):
    def __init__(self):
        self.decoder = adafruit_irremote.GenericDecode()
        # Measuring IR pulses
        self.pulsein = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
    def get_pulses(self, blocking=False):
        pulses = self.decoder.read_pulses(self.pulsein, blocking=blocking)
        if pulses:
            print("Heard", len(pulses), "Pulses:", pulses)
            return pulses
        return []
    def get_code(self, pulses):
        if not pulses: return None
        try:
            code = self.decoder.decode_bits(pulses)
            print("Decoded:", code)
            return code
        except adafruit_irremote.IRNECRepeatException:  # unusual short code!
            print("NEC repeat!")
        except adafruit_irremote.IRDecodeException as e:     # failed to decode
            print("Failed to decode: ", e.args)
        return None
class ShittyIr(object):
    def __init__(self):
        self.tx = IrTx()
        self.rx = IrRx()
    def blast(self, pulses):
        if self.tx.is_on():
            self.tx.send_pulses(pulses)
            # blocking flush of the IR just transmitted (it recieves its own signal)
            self.rx.get_pulses(blocking=True)