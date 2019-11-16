# Write your code here :-)
import board
import busio
import random
import time

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    print("trying to lock bus...")



while True:
    hue = round(random.random() * 255)
    print("Asking for color {}".format(hue))
    i2c.writeto(0x42, bytes([hue]))

    print("sleeping...")
    time.sleep(5)
