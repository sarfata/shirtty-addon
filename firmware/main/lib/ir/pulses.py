
from ir.signals import Signals
class Nerf(Signals):
    tolerance = 150 # microseconds
    NERF_TEAM_1 = 'nerf_team_1'
    NERF_TEAM_2 = 'nerf_team_2' 
    _signals = {
        NERF_TEAM_1: [2957, 5996, 2974, 2009, 991, 1987, 987, 2008, 992, 1987, 983, 2008, 1962, 2012, 987, 2008, 966],
        NERF_TEAM_2: [2935, 6037, 2957, 2038, 940, 2047, 961, 2039, 914, 2073, 1957, 2042, 910, 2094, 940, 2042, 936]
    }
class Pulses():
    nerf = Nerf
    @staticmethod
    def match(actual_pulses, debug=False):
        if not actual_pulses: return Signals.UNKNOWN
        nerf = Pulses.nerf.match(actual_pulses, 17, debug)
        if nerf: return nerf
        return Signals.UNKNOWN
