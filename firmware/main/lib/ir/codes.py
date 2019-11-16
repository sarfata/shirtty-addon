from lib.ir.ir import Ir, IrType

class Adafruit(IrType):
    tolerance = 0
    ADAFRUIT_1 = 'adafruit_1'
    ADAFRUIT_2 = 'adafruit_2'
    ADAFRUIT_3 = 'adafruit_3'
    ADAFRUIT_4 = 'adafruit_4'
    ADAFRUIT_5 = 'adafruit_5'
    ADAFRUIT_6 = 'adafruit_6'
    _signals = {
        ADAFRUIT_1: [255, 2, 247, 8],
        ADAFRUIT_2: [255, 2, 119, 136],
        ADAFRUIT_3: [255, 2, 183, 72],
        ADAFRUIT_4: [255, 2, 215, 40],
        ADAFRUIT_5: [255, 2, 87, 168],
        ADAFRUIT_6: [255, 2, 151, 104]
    }

class Codes(Ir):
    adafruit = Adafruit

    @staticmethod
    def match(actual_codes, debug=False):
        adafuit = Codes.adafruit.match(4, actual_codes, debug)
        if adafuit: return adafuit

        return IrType.UKNOWN

SHARP_POWER = 'sharp_power'
VIZIO_POWER = 'vizio_power'