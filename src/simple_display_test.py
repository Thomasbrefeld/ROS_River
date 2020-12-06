#!/usr/bin/env python3
import sys

import board
import time
import neopixel

pixels = neopixel.NeoPixel(board.D18, 256, auto_write=False)
pixels.brightness = .1
try:
	while True:
		for pixel in range(0, 255):
			pixels[pixel] = (pixel, pixel, 255 - pixel)
			pixels.show()
		pixels.fill(0)
		pixels.show()
except Exception as e:
	print(e)
finally:
	pixels.fill(0)
	pixels.show()
