from pixels import ShittyPixels
shit_pixels = ShittyPixels()
shit_pixels.on()
pixels_start_hue = 0

 # elif code_match == Codes.adafruit.ADAFRUIT_3:
    # shit_pixels.toggle()


while True:
    # pixels
    if shit_pixels.is_on():
        for i in range(0, 64, 1):
            row = round(i / 8)
            column = i % 8
            hue = (pixels_start_hue + row / 3 + column / 5) % 6

            rgb = hsl_to_rgb(hue, 1, 0.02)
            shit_pixels.pixels[i] = (round(rgb[0]*255), round(rgb[1]*255), round(rgb[2]*255))

        shit_pixels.pixels.show()
        pixels_start_hue = pixels_start_hue + .3