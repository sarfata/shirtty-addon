from ir.codes import Codes
from ir.pulses import Pulses

def react_to(shit_ir, pulse_reactors={}, code_reactors={}):
        pulses = shit_ir.rx.get_pulses()
        pulse_match = Pulses.match(pulses)
        if pulse_match and pulse_match in pulse_reactors:
            print("PULSE")
            pulse_reactors[pulse_match]()
            return
        code = shit_ir.rx.get_code(pulses)
        code_match = Codes.match(code, debug=True)
        if code_match and code_match in code_reactors:
            print("CODE")
            code_reactors[code_match](code)  
            return