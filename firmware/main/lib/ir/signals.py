
import math

class Signals(object):
    tolerance = 0
    UNKNOWN = None
    @classmethod
    def match(cls, required_len, actual_codes, debug=False):
        if len(actual_codes) != required_len:
            if debug: print("wrong number of codes {}".format(len(actual_codes)))
            return Signals.UNKNOWN
        for kind, code in cls._signals.items():
            if cls.match_against_known(actual_codes, code):
                return kind
        return Signals.UNKNOWN

    @classmethod
    def match_against_known(cls, actual, known_reference, debug=False):
        for i in range(0, len(known_reference), 1):
            if math.fabs(actual[i] - known_reference[i]) > cls.tolerance:
                if debug: print("Signal {} does not match {} vs {}".format(i, actual[i], known_reference[i]))
                return False
        return True
