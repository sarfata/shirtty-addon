from ir.signals import Signals

class Shirtty(Signals):
    COLOR_SYNC = 'color_sync'

    _signals = {
        COLOR_SYNC: lambda actual: len(actual) == 5 and actual[0:4] == [0xde, 0xad, 0xbe, 0xef]
    }

    @classmethod
    def match(cls, actual_codes, debug=False):
        print("Hi!")
        if Shirtty._signals[Shirtty.COLOR_SYNC](actual_codes):
        #  len(actual_codes) == required_len and actual_codes[0:4] == _signals.COLOR_SYNC:
            return Shirtty.COLOR_SYNC
        # elif len(actual_codes) != required_len:
        #     if debug: print("wrong number of codes {}".format(len(actual_codes)))
        #     return IrType.UNKNOWN
        for kind, code in cls._signals.items():
            if cls.match_against_known(actual_codes, code):
                return kind
        return IrType.UNKNOWN

class Adafruit(Signals):
    # Names
    ADAFRUIT_1 = 'adafruit_1'
    ADAFRUIT_2 = 'adafruit_2'
    ADAFRUIT_3 = 'adafruit_3'
    ADAFRUIT_4 = 'adafruit_4'
    ADAFRUIT_5 = 'adafruit_5'
    ADAFRUIT_6 = 'adafruit_6'
    # Signals
    _signals = {
        ADAFRUIT_1: [255, 2, 247, 8],
        ADAFRUIT_2: [255, 2, 119, 136],
        ADAFRUIT_3: [255, 2, 183, 72],
        ADAFRUIT_4: [255, 2, 215, 40],
        ADAFRUIT_5: [255, 2, 87, 168],
        ADAFRUIT_6: [255, 2, 151, 104]
    }

class Sharp(Signals):
    # Names
    POWER = 'power'
    # Signals
    _signals = {
        POWER: [124, 93]
    }

class Vizio(Signals):
    # Names
    POWER = 'power'
    _signals = {
        POWER: [223, 32, 239, 16]
    }

class Codes():
    adafruit = Adafruit
    sharp = Sharp
    vizio = Vizio
    shirtty = Shirtty

    @staticmethod
    def match(actual_codes, debug=False):
        if actual_codes is None: return Signals.UNKNOWN
        adafuit = Codes.adafruit.match(4, actual_codes, debug)
        if adafuit: return adafuit
        shirtty = Codes.shirtty.match(actual_codes)
        if shirtty: return shirtty

        return Signals.UNKNOWN
