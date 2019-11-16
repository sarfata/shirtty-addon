import adafruit_irremote
import pulseio
import board

# No IR Out without an extra capacitor on the power supply
# irtx = pulseio.PWMOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
# irout = pulseio.PulseOut(irtx)

# # Measuring IR pulses
# pulsein = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)

# encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
#                                             zero=[550, 1700], trail=0)
decoder = adafruit_irremote.GenericDecode()

def get_pulses(pulsein):
    pulses = decoder.read_pulses(pulsein, blocking= False)
    if pulses:
        print("Heard", len(pulses), "Pulses:", pulses)
        return pulses
    return []

def get_code(pulses):
    try:
        code = decoder.decode_bits(pulses)
        print("Decoded:", code)
        return code
    except adafruit_irremote.IRNECRepeatException:  # unusual short code!
        print("NEC repeat!")
    except adafruit_irremote.IRDecodeException as e:     # failed to decode
        print("Failed to decode: ", e.args)
    return None