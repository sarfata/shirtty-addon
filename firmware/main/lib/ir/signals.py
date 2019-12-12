import math
class Signals(object):
    tolerance = 0
    UNKNOWN = None
    @classmethod
    def match(cls, actual_codes, required_len=None, debug=False):
        if required_len is not None and len(actual_codes) != required_len:
            if debug: print("wrong number of codes {}".format(len(actual_codes)))
            return Signals.UNKNOWN
        for kind, code in cls._signals.items():
            if cls.match_against_known(actual_codes, code):
                return kind
        return Signals.UNKNOWN
    @classmethod
    def match_against_known(cls, actual, list_or_lambda, debug=False):
        if isinstance(list_or_lambda, list):
            for i in range(0, len(list_or_lambda), 1):
                if math.fabs(actual[i] - list_or_lambda[i]) > cls.tolerance:
                    if debug: print("Signal {} does not match {} vs {}".format(i, actual[i], list_or_lambda[i]))
                    return False
            return True
        # assume lambda actual: return boolean
        return list_or_lambda(actual)
