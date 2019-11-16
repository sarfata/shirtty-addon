from ir.tx import IrTx
from ir.rx import IrRx

class ShittyIr(object):
    def __init__(self):
        self.tx = IrTx()
        self.rx = IrRx()

    def blast(self, pulses):
        if self.tx.is_on():
            self.tx.send_pulses(pulses)
            # blocking flush of the IR just transmitted (it recieves its own signal)
            self.rx.get_pulses(blocking=True)