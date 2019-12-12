import neopixel
import board
class ShittyPixels():
    def __init__(self):
        self.pixels = None
    def on(self):
        self.pixels = neopixel.NeoPixel(board.D4, 64, auto_write=False)
    def off(self):
        self.pixels.deinit()
        self.pixels = None
    def is_on(self):
        return self.pixels is not None
    def toggle(self):
        if self.is_on():
            print("Neo Off!")
            self.off()
        else:
            print("Neo On!")
            self.on()