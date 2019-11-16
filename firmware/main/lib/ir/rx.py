import adafruit_irremote
import pulseio
import board

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