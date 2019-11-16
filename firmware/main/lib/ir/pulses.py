
import math

class Kind():
    NERF_TEAM_1 = 'nerf_team_1'
    NERF_TEAM_2 = 'nerf_team_2'

    SHARP_POWER = 'sharp_power'
    VIZIO_POWER = 'vizio_power'

    ADAFRUIT_1 = 'adafruit_1'

    UNKNOWN = None

class Nerf():
    _team_1 = [2957, 5996, 2974, 2009, 991, 1987, 987, 2008, 992, 1987, 983, 2008, 1962, 2012, 987, 2008, 966]
    _team_2 = [2935, 6037, 2957, 2038, 940, 2047, 961, 2039, 914, 2073, 1957, 2042, 910, 2094, 940, 2042, 936]

    @staticmethod
    def match_pulses(pulses):
        if len(pulses) != 17:
            print("Wrong number of pulses {}".format(len(pulses)))
            return Kind.UNKNOWN

        if Pulses.match_against_known_pulse(pulses, Nerf._team_1):
            return Kind.NERF_TEAM_1
        if Pulses.match_against_known_pulse(pulses, Nerf._team_2):
            return Kind.NERF_TEAM_2

        return Kind.UNKNOWN

class Pulses():
    kind = Kind
    nerf = Nerf
    tolerance = 150 # microseconds
    @staticmethod
    def match_against_known_pulse(actual_pulses, known_reference_pulses):
        for i in range(0, len(known_reference_pulses), 1):
            if math.fabs(actual_pulses[i] - known_reference_pulses[i]) > Pulses.tolerance:
                print("Pulse {} does not match {} vs {}".format(i, actual_pulses[i], known_reference_pulses[i]))
                return False
        return True

def analyse_badge_pulse():
    l = [2151, 1960, 2074, 2016, 2152, 1960, 2130, 1961, 2155, 1961, 2126, 1961, 2151, 1966, 2099, 1987, 2151, 1965, 2125, 1961, 2122, 1995, 2125, 1961, 2095, 1995, 2152, 1960, 2070, 2017, 2130, 1987, 2069, 2017, 2131, 1986, 2099, 1991, 2151, 1961, 2099, 1991, 2125, 1987, 2099, 1991, 2121, 1991, 2099, 1991, 2121, 1991, 2104, 1987, 2121, 1992, 2099, 1991, 2095, 1992, 2129, 1987, 2069, 2017, 2126, 1991, 2095, 1991, 2130, 1986, 2100, 1991, 2121, 1991, 2126, 1960, 2152, 1964, 2100, 1986, 2126, 1990, 2100, 1987, 2095, 2021, 2100, 1986, 2096, 1995, 2121, 1991, 2095, 1995, 2122, 1991, 2096, 1995, 2122, 1991, 2096, 1995, 2121, 1992, 2095, 1995, 2122, 1991, 2096, 1991, 2121, 1996, 2095, 1991, 2122, 1995, 2096, 1991, 2095, 2021, 2092, 1995, 2092, 1995, 2122, 2020, 2066, 1996, 2117, 2022, 2044, 2043, 2095, 2022, 2065, 2021, 2096, 2017, 2069, 2022, 2095, 2017, 2070, 2021, 2095, 2019, 2065, 2021, 2070, 2048, 2065, 2030, 2057, 2051, 2065, 2022, 2065, 2025, 2091, 2022, 2065, 2021, 2070, 2047, 2040, 2050, 2062, 2051, 2039, 2048, 2065, 2051, 2040, 2073, 2039, 2073, 2014, 2077, 2039, 2073, 2013, 2078, 2035, 2077, 2013, 2077, 2009, 2078, 2039, 2103, 1984, 2077, 2040, 2099, 1987, 2104, 2009, 2133, 1957]
    avg = sum(l) / float(len(l))
    print(avg)